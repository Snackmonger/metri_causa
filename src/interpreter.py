# pylint:disable=missing-function-docstring,invalid-name,missing-class-docstring
from loguru import logger
from src.constants import (
    AMBIGUOUS_VOWELS,
    Scansion,
    LONG_VOWELS,
    SHORT_VOWELS
)
from src.nodes import (
    Coda,
    Line,
    Nucleus,
    Onset,
    Rhyme,
    Syllable,
    Word
)
from src.utils import (
    forms_closed_word,
    forms_mutation_environment,
    is_muta_cum_liquida,
    is_open,
    has_next,
    has_onset
)


class LengthInterpreter:
    """
    Open syllables have their surface quantities, or are ambiguous.

    In general, any closed syllable is long. At word-end, however, the 
    coda includes all remaining consonants, even if they would actually be
    syllabified with a following vowel.

    For example, we syllabify
        Πρῶτον ἔχει Κρονίωνα, κερασφόρον ἅρπαγα νύμφης,

    as
        Πρῶ.τον ἔ.χει Κρο.νί.ω.να[,] κε.ρασ.φό.ρον ἅρ.πα.γα νύμ.φης[,]

    when it should really be
        Πρῶ.το.νἔ.χειΚ.ρο.νί.ω.να[,].κε.ρασ.φό.ρο.νἅρ.πα.γα.νύμ.φης[,]

    Therefore, we will say that the last syllable of a word may be "hidden"
    because it requires consideration of the next onset in order to 
    contextualize its length.

    Apart from this, an open syllable may also have a different quantity
    than its surface quantity when it is followed by vowel. When a vowel
    stands in elision or synizesis, it is ignored in scansion. When a 
    vowel stands in correption, it changes from long to short. When a 
    vowel stands in hiatus, no change occurs. 
    """

    def visit_Onset(self, segment: Onset) -> int:
        return len(segment.cluster)

    def visit_Nucleus(self, segment: Nucleus) -> Scansion:

        vowel = segment.vowel.lexeme
        if len(vowel) > 1:
            return Scansion.LONG
        if vowel in LONG_VOWELS:
            return Scansion.LONG
        if vowel in SHORT_VOWELS:
            return Scansion.SHORT
        if vowel in AMBIGUOUS_VOWELS:
            return Scansion.AMBIGUOUS
        logger.info(f"Vowel {vowel} was not recognized.")
        return Scansion.AMBIGUOUS

    def visit_Coda(self, segment: Coda) -> int:
        return len(segment.cluster)

    def visit_Rhyme(self, segment: Rhyme) -> Scansion:
        if segment.coda.cluster:
            return Scansion.LONG

        return segment.nucleus.accept(self)

    def visit_Syllable(self, segment: Syllable) -> Scansion:
        return segment.rhyme.accept(self)

    def visit_Word(self, segment: Word) -> list[Scansion]:
        """Interpret a word.
        
        If any vowel is followed immediately by another vowel, it might be 
        involved in a vowle mutation such as synizesis or correption.
        """
        pattern: list[Scansion] = []
        for i, syllable in enumerate(segment.syllables):
            length = syllable.accept(self)

            # Open syllables might be modified by a following vowel in 
            # correption or synizesis. Keep their surface quantity and 
            # mark them as mutable.
            if is_open(syllable):
                if has_next(segment.syllables, i):
                    next_syllable = segment.syllables[i + 1]
                    if not has_onset(next_syllable):
                        length = Scansion(length.value + "_mutable")

            # Closed syllables are long, but a stop followed by a resonant
            # might count as a single consonant and form a compound onset
            # with the following vowel. We only really care about cases
            # where a non-long vowel might be lengthened.
            elif has_next(segment.syllables, i):
                next_syllable = segment.syllables[i + 1]
                vowel = syllable.rhyme.nucleus.vowel.lexeme
                if is_muta_cum_liquida(syllable, next_syllable) and not vowel in LONG_VOWELS:
                        length = Scansion.MCL
                        
            pattern.append(length)
        return pattern

    def visit_Line(self, segment: Line) -> list[list[Scansion]]:
        """Interpret a line. If any word is immediately followed by another word,
        its final syllable might be affected by the onset of the following word.
        """
        patterns: list[list[Scansion]] = []
        for i, word in enumerate(segment.words):
            pattern = word.accept(self)
            if has_next(segment.words, i):
                next_word = segment.words[i + 1]
                # Check 'hidden' syllable quantity.
                # τὸν κε.μὰς -> Ends with closed syll, and forms genuine 
                # closed word (τὸν.κε.μὰς)
                # Πρῶ.τον ἔ.χει -> Ends with closed syll, but forms
                # open word with next word's onset (Πρῶ.το.νἔ.χει)
                # ὦ Φρύ.γι.ε Ζεῦ -> Ends with open short vowel, but forms
                # closed word with the next word's onset (Φρύ.γι.εΣ.Δεῦ)
                if forms_closed_word(word, next_word):
                    vowel = word.syllables[-1].rhyme.nucleus.vowel.lexeme

                    if is_muta_cum_liquida(word.syllables[-1], next_word.syllables[0]) and not vowel in LONG_VOWELS:
                        pattern[-1] = Scansion.MCL
                    else:
                        pattern[-1] = Scansion.LONG

                else: # forms open word
                    vowel = word.syllables[-1].rhyme.nucleus
                    pattern[-1] = vowel.accept(self)

                if forms_mutation_environment(word, next_word):
                    pattern[-1] = Scansion(pattern[-1].value + "_mutable")
                    
            patterns.append(pattern)
        return patterns
