# lexer.py
"""Lexer (tokenizer) for the MiniLang interpreter."""

from .errors import LexerError
from .tokens import (
    Token, KEYWORDS, INTEGER, PLUS, MINUS, MUL, DIV,
    LPAREN, RPAREN, LET, ID, ASSIGN, IF, ELSE, WHILE,
    PRINT, STRING, FOR, SEMI, TRUE, FALSE, LBRACE,
    RBRACE, LT, GT, EQ, NEQ, EOF, COMMA
)


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
    
    def skip_comment(self):
        """
        Consumes characters until the end of the line.
        Used for ignoring comments starting with '#'.
        """
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        # We don't need to skip the newline explicitly here; 
        # the skip_whitespace() in the next loop iteration will handle it.

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

    def get_string(self):
        """
        Handles strings like "Hello World".
        It consumes the first ", reads the content, and consumes the closing ".
        """
        result = ''
        self.advance() # Skip the opening quote "
        
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
            
        # If we ran out of code before finding a closing quote
        if self.current_char is None:
            self.error() # Or raise a specific error: "Unterminated string"
            
        self.advance() # Skip the closing quote "
        
        return Token(STRING, result)
    
    def peek(self):
        """Look at the next character without consuming it."""
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]
    
    def peek_token(self):
        """
        Calculates the next token without actually consuming it
        or moving the lexer position permanently.
        """
        # 1. Save the current state of the lexer
        old_pos = self.pos
        old_char = self.current_char
        
        # 2. Get the next token (this moves the internal pointer)
        token = self.get_next_token()
        
        # 3. Restore the saved state
        self.pos = old_pos
        self.current_char = old_char
        
        return token

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
            
            if self.current_char == '#':
                self.skip_comment()
                continue
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == '"':
                return self.get_string()
            
            if self.current_char == '=':
                if self.peek() == '=':  # Check for '=='
                    self.advance()
                    self.advance()
                    return Token(EQ, '==')
                else:  # It's just '='
                    self.advance()
                    return Token(ASSIGN, '=')
            
            # New check for '!='
            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(NEQ, '!=')
                else:
                    self.error()  # We don't support '!' by itself

            # New checks for < and >
            elif self.current_char == '<':
                self.advance()
                return Token(LT, '<')

            elif self.current_char == '>':
                self.advance()
                return Token(GT, '>')
            
            # Check for operators
            elif self.current_char == '+':
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
            
            elif self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')

            elif self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')
            
            elif self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            elif self.current_char == '[':
                self.advance()
                return Token(LBRACKET, '[')
            
            elif self.current_char == ']':
                self.advance()
                return Token(RBRACKET, ']')
            
            self.error()
            
            # This part will become an error handler later
            self.error()
        
        # End of file
        return Token(EOF, None)
    
    def error(self):
        # Raise our new, specific error
        raise LexerError(f"Invalid character: '{self.current_char}'")

