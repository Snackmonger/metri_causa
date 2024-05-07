from enum import StrEnum, auto


class TokenType(StrEnum):
    """Lexical token categories."""
    PUNCTUATION = auto()
    STOP = auto()
    DOUBLE = auto()
    RESONANT = auto()
    SIBILANT = auto()
    VOWEL = auto()
    EOF = auto()
    UNKNOWN_LEXEME = auto()
    NEWLINE = auto()
    WORD_BEGIN = auto()
    WORD_END = auto()
    WHITESPACE = auto()



