"""Syllable segment node classes."""
# pylint:disable=missing-function-docstring,invalid-name,missing-class-docstring,too-few-public-methods
from dataclasses import dataclass
from typing import Any, Optional, Protocol
from src.bases import Token


class NodeVisitor(Protocol):
    """Interface contract for interpreting segment nodes."""

    def visit_Onset(self, segment: "Onset") -> Any:
        raise NotImplementedError

    def visit_Nucleus(self, segment: "Nucleus") -> Any:
        raise NotImplementedError

    def visit_Coda(self, segment: "Coda") -> Any:
        raise NotImplementedError

    def visit_Rhyme(self, segment: "Rhyme") -> Any:
        raise NotImplementedError

    def visit_Syllable(self, segment: "Syllable") -> Any:
        raise NotImplementedError

    def visit_Word(self, segment: "Word") -> Any:
        raise NotImplementedError
    
    def visit_Line(self, segment: "Line") -> Any:
        raise NotImplementedError


class Node():
    """Node base class."""

    def accept(self, visitor: NodeVisitor) -> Any:
        """Accept a visitor."""
        raise NotImplementedError


@dataclass
class Onset(Node):
    cluster: list[Token]

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_Onset(self)


@dataclass
class Nucleus(Node):
    vowel: Token

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_Nucleus(self)


@dataclass
class Coda(Node):
    cluster: list[Token]

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_Coda(self)


@dataclass
class Rhyme(Node):
    nucleus: Nucleus
    coda: Coda

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_Rhyme(self)


@dataclass
class Syllable(Node):
    onset: Onset
    rhyme: Rhyme

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_Syllable(self)


@dataclass
class Word(Node):
    syllables: list[Syllable]
    punctuation: Optional[Token]

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_Word(self)

@dataclass
class Line(Node):
    words: list[Word]

    def accept(self, visitor: NodeVisitor) -> Any:
        return visitor.visit_Line(self)

