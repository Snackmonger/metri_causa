# pylint-disable:too-many-branches
from typing import Optional

from src import utils
from src.bases import Tokenizer, Token
from src.constants import ELISION
from src.token_types import TokenType
from src.utils import (
    can_form_diphthong,
    is_stop,
    is_double,
    is_resonant,
    is_sibilant,
    is_vowel,
    is_punctuation,
    is_valid_char
)


class GreekTokenizer(Tokenizer):
    """Tokenizer for Greek text.

    This tokenizer is fairly generic. All characters will be sorted into basic
    1:1 categories, except that diphthongs will be counted as a single token.
    The tokenizer will consider diacriticals in deciding whether a sequence of
    vowels should be a diphthong, so ``αί`` will be a single token, but ``άι`` 
    and ``αϊ`` will be two tokens.
    """

    def __init__(self):
        super().__init__()
        self.__errors: list[str] = []

    def __add_token(self, token_type: TokenType, lexeme: Optional[str] = None) -> None:
        lexeme = lexeme if isinstance(
            lexeme, str) else self.text[self.start: self.current]
        token = Token(token_type, lexeme)
        self.tokens.append(token)
        if token_type == TokenType.UNKNOWN_LEXEME:
            self.__errors.append(
                f"Unknown lexeme: {lexeme} @ {self.line}.{self.line_chars}")

    @property
    def errors(self) -> list[str]:
        """Return the list of errors generated by the tokenization.

        Errors will be any character that is not a Greek letter,
        punctuation mark, whitespace, editorial symbol, or newline.
        Errors are ignored during tokenization but can be reviewed
        for test purposes.
        """
        return self.__errors

    def __fixlines(self, tokens: list[Token]) -> list[list[Token]]:
        """Attempt to organize the stream into lines and remove any
        redundant tokens.
        """
        filtered: list[list[Token]] = [[]]
        lines = 0
        for token in tokens:
            if token.token_type == TokenType.EOF:
                filtered[lines].append(token)
                break
            if token.token_type == TokenType.NEWLINE:
                lines += 1
                filtered.append([])
            if token.token_type == TokenType.WHITESPACE:
                pass
            elif token.token_type == TokenType.UNKNOWN_LEXEME:
                pass
            else:
                filtered[lines].append(token)

        filtered = [x for x in filtered if len(x) > 1]
        return filtered

    def tokenize(self, text: str) -> list[list[Token]]:
        """Tokenize an input text of ancient Greek text.

        Token Types::

            Vowels (simple and diphthong)
            Double Consonants (psi, xi, zeta)
            Resonant Consonants (rho, lambda, mu, nu)
            Stop Consonants (any other consonant)
            Sibilant (sigma)
        Unknown Lexeme::

            If the lexeme is not recognized as a Greek letter, 
            punctuation, space, newline, or special editorial 
            symbol (e.g. obelus), then it will be added to a 
            list of errors and ignored in tokenization.
        Broken Lines::

            If the metrical colon of the poetic line exceeds 
            the page line length, they can be displaced onto 
            the next line without counting the linebreak by 
            using the "-" character like this:

                            ... καὶ γὰρ βια-    (10)
                τὰς Ἄρης ...

            Everything between the "-" and the newline will be 
            ignored, and these two lines will be parsed as if 
            one single line:

                καὶ γὰρ βιατὰς Ἄρης
        """
        self.text: str = text
        self.current: int = 0
        self.start: int = 0
        self.tokens: list[Token] = [Token(TokenType.WORD_BEGIN, "")]

        while not self.is_at_end:
            self.start = self.current
            self.__scan_token()
        self.tokens.append(Token(TokenType.WORD_END, ""))
        self.tokens.append(Token(TokenType.EOF, ""))
        return self.__fixlines(self.tokens)

    def __wrap_ends(self, token_type: TokenType, char: str) -> None:
        self.__add_token(TokenType.WORD_END, "")
        self.__add_token(token_type, char)
        self.__add_token(TokenType.WORD_BEGIN, "")

    def __scan_token(self) -> None:
        char: str = self.advance()

        if char == " " and is_valid_char(self.peek):
            self.__wrap_ends(TokenType.WHITESPACE, char)

        elif char == "-":
            # Symbol indicates that a metrical colon is broken across multiple
            # printed lines. Ignore all lexemes until we find the line break,
            # then resume normal tokenizing.
            while self.previous != "\n":
                self.advance()

        elif char == "\n":
            # Token ostensibly indicates the end of a metrical colon.
            self.line += 1
            self.line_chars = 0
            self.__wrap_ends(TokenType.NEWLINE, "\\n")

        elif is_vowel(char):
            self.__vowel()

        elif is_stop(char):
            self.__stop()

        elif is_resonant(char):
            self.__resonant()

        elif is_double(char):
            self.__double()

        elif is_sibilant(char):
            self.__sibilant()

        elif is_punctuation(char):
            self.__add_token(TokenType.PUNCTUATION, char)

        elif char == ELISION:
            self.__add_token(TokenType.ELISION, char)

        elif char in "\t\r\b\f\v":
            pass

        else:
            self.__add_token(TokenType.UNKNOWN_LEXEME, char)

    def __check_digraph(self) -> bool:
        char = self.previous
        next_ = self.peek
        if can_form_diphthong(char, next_):
            self.advance()
            return True
        return False

    def __stop(self) -> None:
        self.__add_token(TokenType.STOP)

    def __resonant(self) -> None:
        self.__add_token(TokenType.RESONANT)

    def __sibilant(self) -> None:
        self.__add_token(TokenType.SIBILANT)

    def __double(self) -> None:
        # double consonants are broken into their constituent phonemes
        # so that we can represent a syllable boundary between them.
        c1, c2 = utils.break_double(self.previous)
        self.tokens.append(c1)
        self.tokens.append(c2)

    def __vowel(self) -> None:
        self.__check_digraph()
        self.__add_token(TokenType.VOWEL)
