
from typing import Optional

from loguru import logger

from src.bases import Parser, Token
from src.nodes import (
    Coda,
    Line,
    Nucleus,
    Onset,
    Rhyme,
    Syllable,
    Word
)
from src.token_types import TokenType
from src.utils import is_consonant


class GreekSyllableParser(Parser):
    """Syllable parser for ancient Greek."""

    def parse(self, lines: list[list[Token]]) -> list[Line]:
        """Parse a 2-dimensional array of tokens into a 1-dimensional
        array of Line nodes.
        """
        newlines: list[Line] = []
        for line in lines:
            newlines.append(Line(self.parse_line(line)))
        return newlines

    def parse_line(self, tokens: list[Token]) -> list[Word]:
        """Parse a stream (line) of tokens in ancient Greek."""
        self.start = 0
        self.current = 0
        self.tokens = tokens
        words: list[Word] = []
        while not self.is_at_end:
            if self.match(TokenType.NEWLINE):
                pass
            if (word := self.__word()):
                words.append(word)
        return words

    def __word(self) -> Word:
        self.consume(TokenType.WORD_BEGIN, "Expect word beginning.")
        syllables: list[Syllable] = []
        punct: Optional[Token] = None
        while not self.match(TokenType.WORD_END):
            if self.match(TokenType.PUNCTUATION):
                punct = self.previous
                self.consume(TokenType.WORD_END,
                             "Expect word end after punctuation mark.")
                break
            syllable = self.__syllable()
            syllables.append(syllable)

        return Word(syllables, punct)

    def __syllable(self) -> Syllable:
        onset: Onset = self.__onset()
        rhyme: Rhyme = self.__rhyme()
        return Syllable(onset, rhyme)

    def __onset(self) -> Onset:
        cluster = self.__cluster(True)
        return Onset(cluster)

    def __rhyme(self) -> Rhyme:
        nucleus: Nucleus = self.__nucleus()
        coda: Coda = self.__coda()
        return Rhyme(nucleus, coda)

    def __nucleus(self) -> Nucleus:
        if self.match(TokenType.VOWEL):
            return Nucleus(self.previous)
        if self.match(TokenType.ELISION):
            return Nucleus(self.previous)
        raise RuntimeError(f"Unknown nucleus: {self.peek}. Current: {self.current}")


    def __coda(self) -> Coda:
        if self.__has_another_vowel:
            # VCV should be syllabified as V.CV rather than VC.V
            if is_consonant(self.peek.lexeme) and self.peek_next and self.peek_next.token_type == TokenType.VOWEL:
                return Coda([])
            # VCCV should be syllabified as VC.CV
            return Coda(self.__cluster(greedy=False))
        # VCC[END] should syllabify all remaining consonants in the word (we
        # pretend that words syllabify in isolation from other words and let
        # the interpreter correct them if necessary).
        return Coda(self.__cluster(greedy=True))

    def __cluster(self, greedy: bool = False) -> list[Token]:
        """Create a consonantal segment.

        By default, this will consume the next SINGLE consonant. The 
        ``greedy`` flag indicates to consume ALL following consonants.
        """
        if greedy:
            return self.__greedy()
        if is_consonant(self.peek.lexeme):
            return [self.advance()]
        return []

    def __greedy(self) -> list[Token]:
        """Collect as many consonants as possible in a cluster."""
        cluster: list[Token] = []
        while is_consonant(self.peek.lexeme):
            cluster.append(self.advance())
        return cluster

    @property
    def __has_another_vowel(self) -> bool:
        """Test whether the word to which the current index belongs has 
        another vowel before the word end.

        Coda will normally have 1 consonant, but at word-end it might have more.
        """
        for i in range(self.current, len(self.tokens) - 1):
            if self.tokens[i].token_type == TokenType.VOWEL:
                return True
            if self.tokens[i].token_type == TokenType.WORD_END:
                return False
        return False
