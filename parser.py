# parser.py
"""Parser for the MiniLang interpreter."""

from .errors import ParserError
from .tokens import (
    INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN,
    LET, ID, ASSIGN, IF, ELSE, WHILE, PRINT, STRING,
    FOR, SEMI, TRUE, FALSE, LBRACE, RBRACE, GT, LT,
    EQ, NEQ, EOF, DEF, RETURN, COMMA
)
from .ast_nodes import (
    BinOp, Num, VarDecl, Var, Bool, Block, IfNode,
    WhileNode, PrintNode, AssignNode, String,
    FunctionCallNode, FunctionDefNode, ReturnNode
)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # Set the first token from the lexer
        self.current_token = self.lexer.get_next_token()
    
    def peek(self):
        """Peek at the next token (for parsing blocks)"""
        # This requires the lexer to be able to peek, or
        # we can just look at the current token.
        # Let's just use current_token.
        return self.current_token.type

    def error(self):
        # Raise our new, specific error
        raise ParserError(f"Invalid syntax: Unexpected token {self.current_token}")

    def eat(self, token_type):
        """
        Checks if the current token matches the expected type.
        If it does, it "eats" it and advances to the next token.
        If not, it raises a specific ParserError.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            # This is the new, more helpful error!
            raise ParserError(f"Expected token {token_type}, but found {self.current_token.type}")

    def primary(self):
        """primary : INTEGER | ID | TRUE | FALSE | LPAREN expr RPAREN"""
        token = self.current_token

        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr() 
            self.eat(RPAREN)
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == STRING:
            self.eat(STRING)
            return String(token)
        elif token.type == ID:
            # We assume it's a variable first...
            id_token = self.current_token
            self.eat(ID)
            
            # ...but if we see '(', it's actually a function call!
            if self.current_token.type == LPAREN:
                self.eat(LPAREN)
                args = []
                if self.current_token.type != RPAREN:
                    args.append(self.expr())
                    while self.current_token.type == COMMA:
                        self.eat(COMMA)
                        args.append(self.expr())
                self.eat(RPAREN)
                return FunctionCallNode(id_token.value, args)
            else:
                # It was just a variable
                return Var(id_token)
        elif token.type == TRUE:
            self.eat(TRUE)
            return Bool(token)
        elif token.type == FALSE:
            self.eat(FALSE)
            return Bool(token)
        
        else:
            self.error()

    def term(self):
        """Parses a 'term'. A term is a sequence of factors
           multiplied or divided."""
        node = self.primary() # Get the first factor

        # As long as we see a * or / token, we keep parsing
        while self.current_token.type in (MUL, DIV):
            op_token = self.current_token
            if op_token.type == MUL:
                self.eat(MUL)
            elif op_token.type == DIV:
                self.eat(DIV)
            
            # Get the next factor and create a BinOp node
            # This links the previous 'node' as the left child
            # and the new factor as the right child.
            node = BinOp(left=node, op=op_token, right=self.primary())

        return node
    
    def comparison(self):
        """comparison : term ((GT | LT | EQ | NEQ) term)*"""
        node = self.term()
        while self.current_token.type in (GT, LT, EQ, NEQ):
            op_token = self.current_token
            self.eat(op_token.type)
            node = BinOp(left=node, op=op_token, right=self.term())
        return node
    
    def var_declaration(self):
        """var_declaration : LET ID ASSIGN expr"""
        self.eat(LET)
        var_node = Var(self.current_token)
        self.eat(ID)
        self.eat(ASSIGN)
        value_node = self.expr()
        return VarDecl(var_node, value_node)

    def expr(self):
        """Parses an 'expression'. An expression is a sequence of
           terms added or subtracted."""
        
        # Start by parsing the first term
        node = self.comparison()

        # As long as we see a + or - token, we keep parsing
        while self.current_token.type in (PLUS, MINUS):
            op_token = self.current_token
            if op_token.type == PLUS:
                self.eat(PLUS)
            elif op_token.type == MINUS:
                self.eat(MINUS)

            # Get the next term and create a BinOp node
            # This links the previous 'node' (which could be a
            # complex tree) as the left child.
            node = BinOp(left=node, op=op_token, right=self.comparison())

        return node
    
    def block(self):
        """block : LBRACE statement_list RBRACE"""
        self.eat(LBRACE)
        block_node = Block()
        while self.current_token.type != RBRACE and self.current_token.type != EOF:
            block_node.statements.append(self.statement())
        self.eat(RBRACE)
        return block_node
    
    def if_statement(self):
        """if_statement : IF LPAREN expr RPAREN block (ELSE block)?"""
        self.eat(IF)
        self.eat(LPAREN)
        condition = self.expr()
        self.eat(RPAREN)
        
        then_block = self.block()
        else_block = None
        
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            else_block = self.block()
            
        return IfNode(condition, then_block, else_block)
    
    def while_statement(self):
        """while_statement : WHILE LPAREN expr RPAREN block"""
        self.eat(WHILE)
        self.eat(LPAREN)
        condition = self.expr()
        self.eat(RPAREN)
        
        body = self.block()
        
        return WhileNode(condition, body)
    
    def for_statement(self):
        """
        Parses a for loop: for (init; condition; increment) { body }
        And desugars it into a while loop block.
        """
        self.eat(FOR)
        self.eat(LPAREN)
        
        # 1. Parse the Initialization (e.g., let i = 0)
        # We assume it must be a 'let' statement for now
        if self.current_token.type == LET:
            init_node = self.var_declaration()
        else:
            # Optional: Allow assignment (i = 0) too if you want
            init_node = self.assignment()
            
        self.eat(SEMI) # Eat the first ;
        
        # 2. Parse the Condition (e.g., i < 10)
        condition_node = self.expr()
        
        self.eat(SEMI) # Eat the second ;
        
        # 3. Parse the Increment (e.g., i = i + 1)
        increment_node = self.assignment()
        
        self.eat(RPAREN)
        
        # 4. Parse the Body
        body_node = self.block()
        
        # --- THE MAGIC (Desugaring) ---
        
        # Create a new list of statements for the loop body
        # It includes the original body...
        new_body_statements = body_node.statements[:]
        
        # ...PLUS the increment instruction at the very end
        new_body_statements.append(increment_node)
        
        # Create a new Block for the while loop to use
        new_body = Block()
        new_body.statements = new_body_statements
        
        # Create the WhileNode
        while_node = WhileNode(condition_node, new_body)
        
        # Finally, wrap the INIT and the WHILE inside a parent Block
        # so they execute together
        wrapper_block = Block()
        wrapper_block.statements = [init_node, while_node]
        
        return wrapper_block

    def statement(self):
        """statement : IF ... | WHILE ... | PRINT ... | LET ... | expr"""
        if self.current_token.type == IF:
            return self.if_statement()
        elif self.current_token.type == WHILE: # New check
            return self.while_statement()
        elif self.current_token.type == PRINT: # New check
            return self.print_statement()
        elif self.current_token.type == LET:
            return self.var_declaration()
        # If it's an ID, check if the NEXT token is '='
        elif self.current_token.type == ID and self.lexer.peek_token().type == ASSIGN:
            return self.assignment()
        elif self.current_token.type == FOR: # New check
            return self.for_statement()
        elif self.current_token.type == DEF:     # New
            return self.function_definition()
        elif self.current_token.type == RETURN:  # New
            return self.return_statement()
        else:
            # We'll just parse an expression as a statement
            return self.expr()
    
    def print_statement(self):
        """print_statement : PRINT LPAREN expr RPAREN"""
        self.eat(PRINT)
        self.eat(LPAREN)
        expr = self.expr()
        self.eat(RPAREN)
        return PrintNode(expr)

    def assignment(self):
        """
        Parses assignment: ID ASSIGN expr
        Example: x = x + 1
        """
        # We know the current token is an ID because statement() checked it
        var_node = Var(self.current_token)
        self.eat(ID)
        
        self.eat(ASSIGN)
        
        value_node = self.expr()
        
        return AssignNode(var_node, value_node)

    
    def parse(self):
        """
        parse : statement_list
        Parses multiple statements until EOF and returns a Block containing them.
        For single statements, still returns a Block for consistency.
        """

        #OLD METHOD ONLY PARSE ONE STATEMENT
        # node = self.statement()
        # if self.current_token.type != EOF:
        #     self.error()
        # return node


        #NEW METHOD PARSE MULTIPLE STATEMENTS
        block = Block()
        
        # Parse all statements until EOF
        while self.current_token.type != EOF:
            block.statements.append(self.statement())
        
        # If we have only one statement, we could return it directly,
        # but returning a Block is more consistent and works for both
        # single statements and multiple statements
        return block

    def function_definition(self):
        """def name(param1, param2) { body }"""
        self.eat(DEF)
        
        func_name = self.current_token.value
        self.eat(ID)
        
        self.eat(LPAREN)
        params = []
        if self.current_token.type == ID:
            params.append(self.current_token.value)
            self.eat(ID)
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                params.append(self.current_token.value)
                self.eat(ID)
        self.eat(RPAREN)
        
        body = self.block()
        return FunctionDefNode(func_name, params, body)

    def return_statement(self):
        """return_statement : RETURN expr"""
        self.eat(RETURN)
        expr = self.expr()
        return ReturnNode(expr)
    
    def list_expr(self):
        """Parses [1, 2, 3]"""
        self.eat(LBRACKET)
        elements = []
        if self.current_token.type != RBRACKET:
            elements.append(self.expr())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                elements.append(self.expr())
        self.eat(RBRACKET)
        return ListNode(elements)

