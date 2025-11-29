# tokens.py
"""Token types and Token class for the MiniLang lexer."""

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
IF      = 'IF'
ELSE    = 'ELSE'
WHILE   = 'WHILE'
PRINT   = 'PRINT'
STRING  = 'STRING'
FOR     = 'FOR'
SEMI    = 'SEMI'
DEF     = 'DEF'
COMMA   = 'COMMA'
RETURN  = 'RETURN'
LBRACKET = 'LBRACKET' # [
RBRACKET = 'RBRACKET' # ]
TRUE    = 'TRUE'
FALSE   = 'FALSE'
LBRACE  = 'LBRACE'  # {
RBRACE  = 'RBRACE'  # }
LT      = 'LT'      # <
GT      = 'GT'      # >
EQ      = 'EQ'      # ==
NEQ     = 'NEQ'     # !=
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
    'if': Token(IF, 'if'),
    'else': Token(ELSE, 'else'),
    'while': Token(WHILE, 'while'),
    'print': Token(PRINT, 'print'),
    'for': Token(FOR, 'for'),
    'def': Token(DEF, 'def'),
    'return': Token(RETURN, 'return'),
    'true': Token(TRUE, 'true'),
    'false': Token(FALSE, 'false'),
}

