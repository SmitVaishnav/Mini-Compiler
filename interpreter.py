# interpreter.py
class Error(Exception):
    """Base error class for our interpreter."""
    pass

class LexerError(Error):
    """Error class for the lexer."""
    pass

class ParserError(Error):
    """Error class for the parser."""
    pass
# TOKEN TYPES
# Using strings for these makes debugging easy.
INTEGER = 'INTEGER'
PLUS    = 'PLUS'
MINUS   = 'MINUS'
MUL     = 'MUL'
DIV     = 'DIV'
LPAREN  = 'LPAREN'
RPAREN  = 'RPAREN'
LET     = 'LET'
ID      = 'ID'
ASSIGN  = 'ASSIGN'
EOF     = 'EOF'  # Stands for End Of File



class Token:
    """
    A simple class to hold the token type and its value.
    For example, Token(INTEGER, 5)
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 5)
            Token(PLUS, '+')
        """
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        # The __repr__ method is used for developer-friendly output,
        # which is perfect for our use case.
        return self.__str__()

KEYWORDS = {
    'let': Token(LET, 'let'),
}


# ... (Token Types and Token class from Day 1 are here) ...

###############################################################################
#                                                                             #
#  AST NODES                                                                  #
#                                                                             #
###############################################################################

class AST:
    """Base class for all AST nodes."""
    pass

class BinOp(AST):
    """Represents a binary operation (e.g., 12 + 5)."""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op # The token for the operator, e.g., Token(PLUS, '+')
        self.right = right

class Num(AST):
    """Represents an integer number."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class VarDecl(AST):
    """Represents a variable declaration (e.g., let x = 5)"""
    def __init__(self, var_node, value_node):
        self.var_node = var_node
        self.value_node = value_node

class Var(AST):
    """Represents a variable access (e.g., using 'x' in x + 5)"""
    def __init__(self, token):
        self.token = token
        self.value = token.value




# ... (Lexer class from Day 1 is here) ...
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        # If text is not empty, set the current char, otherwise None
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # We've reached the end
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        # Keep advancing as long as the character is a space
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_integer(self):
        # Keep grabbing digits until the next character is not a digit
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result) # Convert the string of digits to an actual integer

    def get_id(self):
        """Handle identifiers and keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        
        # Check if the identifier is a reserved keyword
        return KEYWORDS.get(result, Token(ID, result))

    def get_next_token(self):
        """Tokenize the input and return the next token."""
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Check for integers
            if self.current_char.isdigit():
                token_value = self.get_integer()
                return Token(INTEGER, token_value)
            
            if self.current_char.isalpha():
                return self.get_id()
            
            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')
            
            # Check for operators
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            elif self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            elif self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            elif self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            # New elif blocks
            elif self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            
            elif self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            # This part will become an error handler later
            self.error()
        
        # End of file
        return Token(EOF, None)
    
    def error(self):
        # Raise our new, specific error
        raise LexerError(f"Invalid character: '{self.current_char}'")


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # Set the first token from the lexer
        self.current_token = self.lexer.get_next_token()

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


    # NEW METHOD: factor
    # This is the highest precedence level.
    # factor : INTEGER
    def factor(self):
        """Parses an INTEGER or a parenthesized expression."""
        token = self.current_token

        if token.type == LPAREN:
            self.eat(LPAREN)
            # Recursively call expr() to parse the sub-expression
            node = self.expr() 
            # After the sub-expression, we must find a closing parenthesis
            self.eat(RPAREN)
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == ID:
            self.eat(ID)
            return Var(token)
        else:
            self.error()

    # NEW METHOD: term
    # This is the middle precedence level.
    # term : factor ((MUL | DIV) factor)*
    def term(self):
        """Parses a 'term'. A term is a sequence of factors
           multiplied or divided."""
        node = self.factor() # Get the first factor

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
            node = BinOp(left=node, op=op_token, right=self.factor())

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
        node = self.term()

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
            node = BinOp(left=node, op=op_token, right=self.term())

        return node

    
    def parse(self):
        """
        parse : var_declaration
              | expr
        """
        # Look at the first token to decide
        if self.current_token.type == LET:
            node = self.var_declaration()
        else:
            node = self.expr()

        # After parsing, we should be at the end of the line
        if self.current_token.type != EOF:
            self.error()
            
        return node

###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class Interpreter:
    def visit(self, node):
        """
        This is the generic visit method that dispatches to the
        correct specific visit method based on the node type.
        For example, if node is a BinOp, it calls self.visit_BinOp(node).
        """
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # This is called if we don't have a specific visitor for a node type.
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_BinOp(self, node):
        """
        Visits a BinOp node. This is the recursive step.
        """
        # We visit the left and right children to get their values
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        # Now we perform the operation based on the operator token
        op_type = node.op.type

        if op_type == PLUS:
            return left_val + right_val
        elif op_type == MINUS:
            return left_val - right_val
        elif op_type == MUL:
            return left_val * right_val
        elif op_type == DIV:
            # Handle division by zero for safety
            if right_val == 0:
                raise Exception("Error: Division by zero")
            return left_val / right_val
    def visit_Num(self, node):
        """
        Visits a Num node. This is the base case of our recursion.
        It just returns the number's value.
        """
        return node.value

# def main():
#     text = "12 + 5 + 3"
#     lexer = Lexer(text)

#     # Let's get all the tokens
#     tokens = []
#     while True:
#         token = lexer.get_next_token()
#         tokens.append(token)
#         if token.type == EOF:
#             break
    
#     print(tokens)

# if __name__ == '__main__':
#     main()



# def main():
#     text = "12 + 5"
#     lexer = Lexer(text)
#     # print(lexer.get_next_token())
#     parser = Parser(lexer)
#     ast = parser.expr() # Get the AST root node

#     # To see the result, we can inspect the AST attributes
#     print("AST Root Node:", type(ast))
#     print("Left child:", ast.left.value)
#     print("Operator:", ast.op.type)
#     print("Right child:", ast.right.value)


# if __name__ == '__main__':
#     main()


def main():
    print("Welcome to the MiniCalc! Type 'exit' or press Ctrl+C to quit.")
    while True:
        try:
            text = input('calc> ')
        # ... (error handling is the same) ...
        except EOFError:
            print("\nExiting.")
            break
        except KeyboardInterrupt:
            print("\nExiting.")
            break

        if not text:
            continue
        if text.strip().lower() == 'exit':
            print("Exiting calculator.")
            break

        

        try: # Add a try/except for our own program errors
            lexer = Lexer(text)
            parser = Parser(lexer)
            # This is the line that changes:
            ast = parser.parse() # Call the new 'parse' method

            # --- TEMPORARY TEST ---
            # Just print the AST for today
            print(f"AST: {type(ast)}")
            if isinstance(ast, VarDecl):
                print(f"  Var Name: {ast.var_node.value}")
                print(f"  Value: {type(ast.value_node)}")
            # --- END TEST ---
            
            # interpreter = Interpreter()
            # result = interpreter.visit(ast)
            # print(result)

        # Catch our specific errors first
        except (LexerError, ParserError) as e:
            print(f"Syntax Error: {e}")
        # Catch other errors like division by zero
        except Exception as e:
            print(f"Runtime Error: {e}")


if __name__ == '__main__':
    main()