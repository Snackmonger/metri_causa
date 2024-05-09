# pylint:disable=too-many-instance-attributes,too-few-public-methods
"""Miscellaneous utilities used in the program."""
from typing import (
    Any,
    Callable,
    Optional,
    Sequence
)
import unicodedata

from loguru import logger
from src.constants import (
    CONSONANTS,
    ELISION,
    LONG_VOWELS,
    SHORT_VOWELS,
    STOPS,
    DOUBLE_CONSONANTS,
    PUNCTUATION,
    RESONANTS,
    RHO_VARIANTS,
    SIGMA_VARIANTS,
    VOWELS,
    Scansion
)
from src.bases import Token
from src.token_types import TokenType
from src.nodes import (
    Syllable,
    Word
)


def strcheck(func: Callable[[str], bool]) -> Callable[[str], bool]:
    """Return False if the given parameter is not a string, or if the string
    is empty."""
    def decorator(char: Optional[str]) -> bool:
        if not isinstance(char, str):
            return False
        if char == "":
            return False
        return func(char)
    return decorator


@strcheck
def is_stop(char: str) -> bool:
    """Test whether a character is a plain consonant."""
    return char in STOPS


@strcheck
def is_vowel(char: str) -> bool:
    """Test whether a character is a vowel."""
    return char in VOWELS


@strcheck
def is_double(char: str) -> bool:
    """Test whether a character is a double consonant."""
    return char in DOUBLE_CONSONANTS


@strcheck
def is_sibilant(char: str) -> bool:
    """Test whether a character is a double consonant."""
    return char in SIGMA_VARIANTS


@strcheck
def is_resonant(char: str) -> bool:
    """Thest whether a character is a resonant consonant."""
    return char in RESONANTS or char in RHO_VARIANTS


@strcheck
def is_punctuation(char: str) -> bool:
    """Test whether the character is punctuation."""
    return char in PUNCTUATION


@strcheck
def is_space(char: str) -> bool:
    """Test whether the character is space."""
    return char == " "


@strcheck
def is_consonant(char: str) -> bool:
    """Test whether the character is a consonant in any class."""
    return char in CONSONANTS


@strcheck
def is_valid_char(char: str) -> bool:
    """Test whether the character is a symbol character (i.e. not a formatting
    or control character).
    """
    return is_consonant(char) or is_vowel(char) or is_punctuation(char)


@strcheck
def can_start_digraph(char: str) -> bool:
    """Check whether the given vowel char is appropriate for beginning a 
    digraph vowel sequence.
    """
    if not is_vowel(char):
        return False
    vowel = VowelGlyph(char)
    if any([vowel.oxia,
            vowel.varia,
            vowel.perispomeni,
            vowel.ypogegrammeni,
            vowel.prosgegrammeni,
            vowel.psili,
            vowel.dasia,
            vowel.iota]):
        return False
    return True


@strcheck
def can_finish_digraph(char: str) -> bool:
    """Check whether the given vowel char is appropriate for ending a
    digraph vowel sequence.
    """
    if not is_vowel(char):
        return False
    vowel = VowelGlyph(char)
    if any([vowel.alpha,
            vowel.omicron,
            vowel.omega,
            vowel.eta,
            vowel.epsilon,
            vowel.dialytika]):
        return False
    return True


def get_char_attrs(char: str) -> list[str]:
    """Return a list of all words that appear in the descriptions of the 
    unicode character.

    E.g.
        ("ὄ") -> ['omicron', 'small', 'psili']
    """
    conversions = {"acute": "oxia",
                   "grave": "varia",
                   "circumflex": "perispomeni",
                   "diaeresis": "dialytika",
                   "breve": "vrachy",
                   "tonos": "oxia"}
    source: str = unicodedata.decomposition(char)
    if source:
        elems: list[str] = []
        for x in source.split(" "):
            if not x == "":
                elems.append(unicodedata.name(chr(int(x, 16))))
        result = [y.lower() for x in elems for y in x.split()]
        for mistake, correction in conversions.items():
            if mistake in result:
                result.append(correction)
        if "comma" in result:
            if "reversed" in result:
                result.append("dasia")
            else:
                result.append("psili")
        return result

    return [x.lower() for x in unicodedata.name(char).split(" ")]


def make_words(tokens: list[Token]) -> list[tuple[Token, ...]]:
    """Split a list of tokens into word groups."""
    tokens = [x for x in tokens if not x.token_type ==
              TokenType.UNKNOWN_LEXEME]
    words: list[tuple[Token, ...]] = []
    consume = False
    word: list[Token] = []
    for token in tokens:
        if token.token_type == TokenType.WORD_BEGIN:
            consume = True
        if token.token_type == TokenType.WORD_END:
            consume = False
            word.append(token)
            words.append(tuple(word))
            word = []
        if consume:
            word.append(token)
    return words


def break_double(char: str) -> list[Token]:
    """Break a double consonant into its constituent consonants and
    return a pair of tokens representing those consonants."""
    if char in "ζΖ":
        return [Token(TokenType.SIBILANT, casematch(char, "Σ")),
                Token(TokenType.STOP, casematch(char, "Δ"))]
    if char in "ξΞ":
        return [Token(TokenType.STOP, casematch(char, "Κ")),
                Token(TokenType.SIBILANT, casematch(char, "Σ"))]
    if char in "ψΨ":
        return [Token(TokenType.STOP, casematch(char, "Π")),
                Token(TokenType.SIBILANT, casematch(char, "Σ"))]
    raise ValueError("Invalid character.")

def join_double(chars: str) -> str:
    """Join two literal characters into their appropriate double character."""
    chars_ = chars.upper()
    match chars_:
        case "ΣΔ":
            return casematch(chars, "Ζ")
        case "ΚΣ":
            return casematch(chars, "Ξ")
        case "ΠΣ":
            return casematch(chars, "Ψ")
        case _:
            raise ValueError(f"Invalid double characters: {chars}")


def casematch(prototype: str, char: str) -> str:
    """Return the given character(s) in the same case as the given prototype."""
    if prototype.isupper():
        return char.upper()
    if prototype.islower():
        return char.lower()
    raise ValueError("Invalid character")


class VowelGlyph():
    """Representation a polytonic Greek vowel glyph, 
    possibly with diacritical marks."""

    def __init__(self, char: str) -> None:
        self.alpha: bool = False
        self.epsilon: bool = False
        self.eta: bool = False
        self.iota: bool = False
        self.omicron: bool = False
        self.omega: bool = False
        self.upsilon: bool = False
        self.small: bool = False
        self.psili: bool = False
        self.dasia: bool = False
        self.varia: bool = False
        self.oxia: bool = False
        self.perispomeni: bool = False
        self.capital: bool = False
        self.ypogegrammeni: bool = False
        self.prosgegrammeni: bool = False
        self.vrachy: bool = False
        self.macron: bool = False
        self.omicron: bool = False
        self.tonos: bool = False
        self.dialytika: bool = False
        self.char: str = char
        self.__populate(char)

    def __populate(self, char: str) -> None:
        for attr in get_char_attrs(char):
            if hasattr(self, attr):
                setattr(self, attr, True)

    def __repr__(self) -> str:
        string = "<:"
        for k, v in vars(self).items():
            if k == "char":
                pass
            if v:
                string += k + ", "
        return string[:-2] + ":>"
    
    def length(self) -> Scansion:
        """Return the natural length of the vowel."""
        if self.perispomeni:
            return Scansion.LONG
        if self.alpha or self.iota or self.upsilon:
            return Scansion.AMBIGUOUS
        if self.eta or self.omega:
            return Scansion.LONG
        if self.epsilon or self.omicron:
            return Scansion.SHORT
        raise ValueError(f"Unknown vowel: {self.char}")
    

def is_open(syllable: Syllable) -> bool:
    """Indicate whether the syllable has a coda."""
    return not bool(syllable.rhyme.coda.cluster)

def has_next(array: Sequence[Any], index: int) -> bool:
    """Indicate whether a word has at least 1 more syllable, considered
    from the given syllable index.
    """
    return index < len(array) - 1

def has_onset(syllable: Syllable) -> bool:
    """Indicate whether the syllable has an onset."""
    return bool(syllable.onset.cluster)

def forms_closed_word(word1: Word, word2: Word) -> bool:
    """Indicate whether the ending of word1 should be considered closed,
    considering the beginning of word2.
    """
    left = word1.syllables[-1]
    right = word2.syllables[0]
    consonants: list[Token] = []
    if (x := left.rhyme.coda):
        consonants.extend(x.cluster)
    if (x := right.onset):
        consonants.extend(x.cluster)
    return len(consonants) > 1
        
def forms_mutation_environment(word1: Word, word2: Word) -> bool:
    """Indicate whether the ending of word1 should be considered a mutable
    vowel, considering the beginning of word2."""
    left = word1.syllables[-1]
    right = word2.syllables[0]
    return is_open(left) and not has_onset(right)

def simplify_metrical_symbols(cola: list[Scansion]) -> list[str]:
    """Take a list of enum values and return simple symbol representations of 
    them.
    """
    values: list[str] = []
    for colon in cola:
        if colon == Scansion.LONG:
            values.append("+")
        if colon == Scansion.LONG_MUTABLE:
            values.append("+*")
        if colon == Scansion.SHORT:
            values.append("-")
        if colon == Scansion.SHORT_MUTABLE:
            values.append("-*")
        if colon == Scansion.AMBIGUOUS:
            values.append("?")
        if colon == Scansion.AMBIGUOUS_MUTABLE:
            values.append("?*")
        if colon == Scansion.MCL:
            values.append("M")
        if colon == Scansion.ELISION:
            values.append("E")
    return values

def is_muta_cum_liquida(syllable1: Syllable, syllable2: Syllable) -> bool:
    """Indicate whether the ending of syllable1 forms a muta-cum-liquida
    environment with the beginning of syllable2.
    """
    consonants: list[Token] = syllable1.rhyme.coda.cluster + syllable2.onset.cluster
    if [x.token_type for x in consonants] == [TokenType.STOP, TokenType.RESONANT]:
        # Any combination of stop + resonant ("liquid") passes the test.
        # The groups "γν", "γμ", "δν", "δμ" are always long in the best poets,
        # but later versifiers sometimes take this license, so we let the
        # interpreter decide whether they're valid clusters for MCL.
        return True
    return False

def ends_with_elision(word: Word) -> bool:
    """Indicate whether the given word ends with an elided vowel."""
    return word.syllables[-1].rhyme.nucleus.vowel.token_type == TokenType.ELISION