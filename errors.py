# errors.py
"""Error classes for the MiniLang interpreter."""


class Error(Exception):
    """Base error class for our interpreter."""
    pass


class LexerError(Error):
    """Error class for the lexer."""
    pass


class ParserError(Error):
    """Error class for the parser."""
    pass

