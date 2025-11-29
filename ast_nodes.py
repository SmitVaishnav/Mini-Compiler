# ast.py
"""Abstract Syntax Tree (AST) node classes for MiniLang."""


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


class Bool(AST):
    """Represents a boolean value (True or False)"""
    def __init__(self, token):
        self.token = token
        self.value = token.value  # TRUE or FALSE


class Block(AST):
    """Represents a block of statements, e.g., { ... }"""
    def __init__(self):
        self.statements = []  # A list of statement nodes


class IfNode(AST):
    """Represents an if or if-else statement"""
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition  # The (x > 5) part
        self.then_block = then_block  # The { ... } part
        self.else_block = else_block  # The optional else { ... } part


class WhileNode(AST):
    """Represents a while loop"""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body # This will be a Block node


class PrintNode(AST):
    """Represents a print statement"""
    def __init__(self, expression):
        self.expression = expression


class AssignNode(AST):
    """Represents a variable assignment (e.g., x = 10)"""
    def __init__(self, var_node, value_node):
        self.var_node = var_node     # The 'x'
        self.value_node = value_node # The '10'


class String(AST):
    """Represents a string value (e.g., "Hello")"""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class FunctionDefNode(AST):
    def __init__(self, name, params, body):
        self.name = name       # String (function name)
        self.params = params   # List of strings (parameter names)
        self.body = body       # Block node

class FunctionCallNode(AST):
    def __init__(self, name, args):
        self.name = name       # String (function name)
        self.args = args       # List of AST nodes (arguments)

class ReturnNode(AST):
    def __init__(self, value_node):
        self.value_node = value_node

class ListNode(AST):
    """Represents a list literal like [1, 2, 3]"""
    def __init__(self, elements):
        self.elements = elements # List of AST nodes

class IndexNode(AST):
    """Represents accessing a list: some_list[index]"""
    def __init__(self, left, index):
        self.left = left   # The list being accessed
        self.index = index # The expression inside [ ]
