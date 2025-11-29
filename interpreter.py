# interpreter.py
"""Interpreter (evaluator) for the MiniLang interpreter."""
import time
import random
import math
from .tokens import PLUS, MINUS, MUL, DIV, EQ, NEQ, LT, GT, ID
from .tokens import Token
from .ast_nodes import (
    BinOp, Num, VarDecl, Var, Bool, Block, IfNode,
    WhileNode, PrintNode, AssignNode, String,
    FunctionCallNode, FunctionDefNode, ReturnNode,
    ListNode, IndexNode
)

class NativeFunction:
    """
    Wraps a Python function so it can be called inside our language.
    """
    def __init__(self, func):
        self.func = func

    def call(self, arguments):
        # We pass the list of arguments to the Python function
        return self.func(arguments)

class Interpreter:
    def __init__(self):
        # This is our 'memory'
        self.scopes = [{}]
        # --- LOAD STANDARD LIBRARY ---
        self.init_stdlib()
    
    def init_stdlib(self):
        # We define lambda functions to bridge the gap between 
        # our list of arguments and what Python expects.
        
        # input(prompt)
        self.scopes[0]['input'] = NativeFunction(
            lambda args: input(str(args[0])) if args else input()
        )
        
        # len(item)
        self.scopes[0]['len'] = NativeFunction(
            lambda args: len(args[0])
        )
        
        # time()
        self.scopes[0]['time'] = NativeFunction(
            lambda args: time.time()
        )
        
        # random() -> returns float between 0.0 and 1.0
        self.scopes[0]['random'] = NativeFunction(
            lambda args: random.random()
        )
        
        # int(value) -> converts string/float to integer
        self.scopes[0]['int'] = NativeFunction(
            lambda args: int(args[0])
        )
        
        # str(value) -> converts to string
        self.scopes[0]['str'] = NativeFunction(
            lambda args: str(args[0])
        )
        # --- END OF STANDARD LIBRARY ---
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
    
    def visit_VarDecl(self, node):
        """
        Visits a VarDecl node.
        This performs the assignment.
        """
        # Get the name of the variable
        var_name = node.var_node.value
        
        # Evaluate the expression on the right side
        value = self.visit(node.value_node)
        
        # Store it in our symbol table
        self.symbol_table[var_name] = value
        
        # Declarations are statements, they don't return a value
        return None
    
    def visit_Var(self, node):
        """
        Visits a Var node.
        This retrieves the variable's value from memory.
        """
        var_name = node.value
        
        # Look up the value in the symbol table
        value = self.symbol_table.get(var_name)
        
        # Handle the case where the variable doesn't exist
        if value is None:
            raise NameError(f"Name '{var_name}' is not defined")
            
        return value

    def visit_String(self, node):
        return node.value
    
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
            # Handle string concatenation (convert numbers to strings if needed)
            if isinstance(left_val, str) or isinstance(right_val, str):
                return str(left_val) + str(right_val)
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
        elif op_type == EQ:
            return left_val == right_val
        elif op_type == NEQ:
            return left_val != right_val
        elif op_type == LT:
            return left_val < right_val
        elif op_type == GT:
            return left_val > right_val


    def visit_AssignNode(self, node):
        """
        Executes an assignment.
        """
        var_name = node.var_node.value
        
        # Evaluate the new value
        value = self.visit(node.value_node)
        
        # Safety Check: Does the variable exist?
        if var_name not in self.symbol_table:
            raise NameError(f"Cannot assign to undefined variable '{var_name}'")
        
        # Update the value
        self.symbol_table[var_name] = value
        
        return None    

    def visit_Num(self, node):
        """
        Visits a Num node. This is the base case of our recursion.
        It just returns the number's value.
        """
        return node.value
    
    def visit_Bool(self, node):
        """Returns the Python boolean True or False"""
        # Our token value is 'true'/'false' string, so we map it to Python bools
        return True if node.value == 'true' else False

    def visit_Block(self, node):
        """Executes a list of statements"""
        for statement in node.statements:
            self.visit(statement)
        return None

    def visit_IfNode(self, node):
        """Handles if/else logic"""
        # 1. Evaluate the condition
        condition_value = self.visit(node.condition)
        
        # 2. Decide which block to run
        if condition_value:
            self.visit(node.then_block)
        elif node.else_block:
            self.visit(node.else_block)
        
        return None
    
    def visit_WhileNode(self, node):
        """
        Executes a while loop.
        """
        # We use Python's own 'while' to repeat the logic
        while self.visit(node.condition):
            # Execute the code inside the loop block
            self.visit(node.body)
        
        return None
    
    def visit_PrintNode(self, node):
        """
        Executes a print statement.
        """
        # 1. Evaluate the expression inside the print()
        value = self.visit(node.expression)
        
        # 2. Use Python's native print to show it
        print(value)
        
        return None

    def current_scope(self):
        return self.scopes[-1]

    def visit_VarDecl(self, node):
        # Always define variables in the CURRENT scope
        var_name = node.var_node.value
        value = self.visit(node.value_node)
        self.current_scope()[var_name] = value
        return None

    def visit_Var(self, node):
        var_name = node.value
        # Look for the variable, starting from current scope and going down
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope[var_name]
        raise NameError(f"Name '{var_name}' is not defined")
        
    def visit_AssignNode(self, node):
        var_name = node.var_node.value
        value = self.visit(node.value_node)
        # Find which scope the variable lives in, and update it there
        for scope in reversed(self.scopes):
            if var_name in scope:
                scope[var_name] = value
                return None
        raise NameError(f"Cannot assign to undefined variable '{var_name}'")
    
    def visit_FunctionDefNode(self, node):
        # A function is just a variable! 
        # We store the function NODE itself in the symbol table.
        func_name = node.name
        self.current_scope()[func_name] = node
        return None

    def visit_ReturnNode(self, node):
        value = self.visit(node.value_node)
        # Throw the value up to the caller
        raise ReturnException(value)

    def visit_FunctionCallNode(self, node):
        func_name = node.name

        # 1. Find the function (It could be Native OR Custom)
        func_obj = self.visit_Var(Var(Token(ID, func_name)))

        # 2. Evaluate Arguments
        arg_values = []
        for arg in node.args:
            arg_values.append(self.visit(arg))

        # --- CASE A: Native Function (Python) ---
        if isinstance(func_obj, NativeFunction):
            return func_obj.call(arg_values)
        
        # --- CASE B: Custom Function (User defined) ---
        if isinstance(func_obj, FunctionDefNode):
            
            # Check arg count
            if len(arg_values) != len(func_obj.params):
                raise Exception(f"Function '{func_name}' expects {len(func_obj.params)} args, got {len(arg_values)}")

            # Create New Scope
            new_scope = {}
            for param_name, arg_val in zip(func_obj.params, arg_values):
                new_scope[param_name] = arg_val
            
            self.scopes.append(new_scope)
            
            result = None
            try:
                self.visit(func_obj.body)
            except ReturnException as e:
                result = e.value
            
            self.scopes.pop()
            return result
        
        raise Exception(f"'{func_name}' is not a function")


        # THE OLD FUNCTION WHERE NATIVE FUNCTIONS WERE NOT USED --------------------------------
        # 1. Find the function definition
        # Look for the function in scopes, starting from current scope
        # func_node = None
        # for scope in reversed(self.scopes):
        #     if func_name in scope:
        #         func_node = scope[func_name]
        #         break
        
        # if func_node is None:
        #     raise NameError(f"Function '{func_name}' is not defined")
        
        # if not isinstance(func_node, FunctionDefNode):
        #      raise Exception(f"'{func_name}' is not a function")
        
        # # 2. Check arg count
        # if len(node.args) != len(func_node.params):
        #     raise Exception(f"Function '{func_name}' expects {len(func_node.params)} args, got {len(node.args)}")

        # # 3. Create a NEW Scope for this function run
        # new_scope = {}
        
        # # 4. Map Arguments (Values) to Parameters (Names)
        # for param_name, arg_node in zip(func_node.params, node.args):
        #     new_scope[param_name] = self.visit(arg_node)
            
        # # 5. Push the new scope onto the stack
        # self.scopes.append(new_scope)
        
        # # 6. Run the body
        # result = None
        # try:
        #     self.visit(func_node.body)
        # except ReturnException as e:
        #     result = e.value
        
        # # 7. Pop the scope (Destroy local variables)
        # self.scopes.pop()
        
        # return result
    
    def visit_ListNode(self, node):
        # Convert [AST, AST] -> [Val, Val]
        elements = []
        for element_node in node.elements:
            elements.append(self.visit(element_node))
        return elements

    def visit_IndexNode(self, node):
        # 1. Evaluate the list (e.g., x -> [1, 2])
        left_val = self.visit(node.left)
        
        # 2. Evaluate the index (e.g., 0)
        idx = self.visit(node.index)
        
        # 3. Validation
        if not isinstance(left_val, list) and not isinstance(left_val, str):
            raise Exception("Type Error: Indexing is only supported for Lists and Strings.")
        
        if not isinstance(idx, int):
            raise Exception("Type Error: Index must be an integer.")
            
        if idx < 0 or idx >= len(left_val):
            raise Exception("Index Error: List index out of range.")
            
        return left_val[idx]


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value