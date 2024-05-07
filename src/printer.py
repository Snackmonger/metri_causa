# pylint:disable=missing-function-docstring,invalid-name,missing-class-docstring
"""Printer for the syllable node tree."""
from src.nodes import (
    Coda,
    Line,
    Onset,
    Rhyme,
    Syllable,
    Nucleus,
    Word
)


class SyllableTreePrinter:
    """Simplifies syllable node string representations."""

    def visit_Onset(self, segment: Onset) -> str:
        return "".join(x.lexeme for x in segment.cluster)

    def visit_Nucleus(self, segment: Nucleus) -> str:
        return segment.vowel.lexeme

    def visit_Coda(self, segment: Coda) -> str:
        return "".join(x.lexeme for x in segment.cluster)

    def visit_Rhyme(self, segment: Rhyme) -> str:
        string = segment.nucleus.vowel.lexeme
        if segment.coda:
            string += segment.coda.accept(self)
        return string

    def visit_Syllable(self, segment: Syllable) -> str:
        string = ""
        if segment.onset:
            string = segment.onset.accept(self)
        string += segment.rhyme.accept(self)
        return string

    def visit_Word(self, segment: Word) -> str:
        optional = f"[{segment.punctuation.lexeme}]" if segment.punctuation else ""
        return ".".join([x.accept(self) for x in segment.syllables]) + optional

    def visit_Line(self, segment: Line) -> str:
        return " ".join(x.accept(self) for x in segment.words)
