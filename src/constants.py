"""Constants used in the program."""
from enum import Enum, StrEnum, auto

ALPHA_VARIANTS = "ἀἁἂἃἄἅἆἇἈἉἊἋἌἍἎἏὰάᾀᾁᾂᾃᾄᾅᾆᾇᾈᾉᾊᾋᾌᾍᾎᾏᾰᾱᾲᾳᾴᾶᾷᾸᾹᾺΆᾼαΑά"
EPSILON_VARIANTS = "ἐἑἒἓἔἕἘἙἚἛἜἝὲέεΕέ"
ETA_VARIANTS = "ἠἡἢἣἥἤἦἧἨἩἪἫἬἭἮἯὴήᾐᾑᾒᾓᾔᾕᾖᾗᾘᾙᾚᾛᾜᾝᾞᾟῂῃῄῆῇῈΈῊΉῌηΗή"
IOTA_VARIANTS = "ἰἱἲἳἴἵἶἷἸἹἺἻἼἽἾἿὶίῐῑῒΐῖῗῘῙῚΊιΙίϊΐ"
OMICRON_VARIANTS = "ὀὁὂὃὄὅὈὉὊὋὌὍὸόόοΟ"
UPSILON_VARIANTS = "ὐὑὒὓὔὕὖὗὙὛὝὟὺύῦῧῨῩῪΎῠῡῢΰυύΥΰϋ"
OMEGA_VARIANTS = "ὠὡὢὣὤὥὦὧὨὩὪὫὬὭὮὯὼώᾠᾡᾢᾣᾤᾥᾦᾧᾨᾩᾪᾫᾬᾭᾮᾯῲῳῴῶῷῸΌῺΏῼωΩώ"
VOWELS = ALPHA_VARIANTS + EPSILON_VARIANTS + IOTA_VARIANTS + OMICRON_VARIANTS \
    + OMEGA_VARIANTS + UPSILON_VARIANTS + ETA_VARIANTS
LONG_VOWELS = ETA_VARIANTS + OMEGA_VARIANTS
SHORT_VOWELS = EPSILON_VARIANTS + OMICRON_VARIANTS
AMBIGUOUS_VOWELS = UPSILON_VARIANTS + IOTA_VARIANTS + ALPHA_VARIANTS
STOPS = "ΒΓΔΘΚΠΣΤΦΧβγδθκπστφχ"
RESONANTS = "λΛμΜνΝρΡ"
RHO_VARIANTS = "ῤῥῬρ"
SIGMA_VARIANTS = "σΣς"
DOUBLE_CONSONANTS = "ζψξΖΨΞ"
ELISION = "’"
PUNCTUATION = "«».,·;"
CONSONANTS = STOPS + RESONANTS + RHO_VARIANTS + SIGMA_VARIANTS + DOUBLE_CONSONANTS

class Scansion(StrEnum):
    """Types of vowel length."""
    LONG = auto()
    SHORT = auto()
    AMBIGUOUS = auto()
    ELISION = auto()
    MCL = auto()
    LONG_MUTABLE = auto()
    SHORT_MUTABLE = auto()
    AMBIGUOUS_MUTABLE = auto()

class HexameterStates(StrEnum):
    """Representation of the finite states in which the hexameter can exist."""
    # 0
    DDDDD =  auto()
    # 1
    SDDDD =  auto()
    DSDDD =  auto()
    DDSDD =  auto()
    DDDSD =  auto()
    DDDDS =  auto()
    # 2
    SSDDD =  auto()
    DSSDD =  auto()
    DDSSD =  auto()
    DDDSS =  auto()
    SDSDD =  auto()
    SDDSD =  auto()
    SDDDS =  auto()
    DSDSD =  auto()
    DDSDS =  auto()
    DSDDS =  auto()
    # 3
    DDSSS =  auto()
    SDDSS =  auto()
    SSDDS =  auto()
    SSSDD =  auto()
    DSDSS =  auto()
    DSSDS =  auto()
    SDSDS =  auto()
    SSDSD =  auto()
    SDSSD =  auto()
    # 4
    DSSSS =  auto()
    SDSSS =  auto()
    SSDSS =  auto()
    SSSDS =  auto()
    SSSSD =  auto()
    # 5
    SSSSS =  auto()

class HexameterBinary(Enum):
    """Representation of the finite states in which the hexameter can exist.
    
    The enum's values are not only unique identifiers of each pattern, they
    also map the pattern so that the binary 0 = dactyl and 1 = spondee.
    """
    # 0 Spondees
    DDDDD = 0b00000
    # 1 Spondee
    SDDDD = 0b10000
    DSDDD = 0b01000
    DDSDD = 0b00100
    DDDSD = 0b00010
    DDDDS = 0b00001
    # 2 Spondees
    SSDDD = 0b11000
    DSSDD = 0b01100
    DDSSD = 0b00110
    DDDSS = 0b00011
    SDSDD = 0b10100
    SDDSD = 0b10010
    SDDDS = 0b10001
    DSDSD = 0b01010
    DDSDS = 0b00101
    DSDDS = 0b01001
    # 3 Spondees
    DDSSS = 0b00111
    SDDSS = 0b10011
    SSDDS = 0b11001
    SSSDD = 0b11100
    DSDSS = 0b01011
    DSSDS = 0b01101
    SDSDS = 0b10101
    SSDSD = 0b11010
    SDSSD = 0b10110
    # 4 Spondees
    DSSSS = 0b01111
    SDSSS = 0b10111
    SSDSS = 0b11011
    SSSDS = 0b11101
    SSSSD = 0b11110
    # 5 Spondees
    SSSSS = 0b11111


# Metrical Symbols in Unicode
# × (multiplication sign) anceps 00D7
# ⏑ metrical breve 23D1
# – (EN dash) longum 2013
# ⏒ metrical long over short 23D2
# ⏓ metrical short over long 23D3
# ⏔ metrical long over two shorts 23D4
# ⏕ metrical two shorts over long 23D5
# ◯◯ Aeolian basis 25EF.25EF
# ⏖ metrical two shorts joined 23D6
# ⌒ brevis in longo 2312̭
# catalexis indicator 0020.032D
# ⁝ tricolon 205D
# | word end indicator 007C
# ‖ period end 2016
# ||| stanza end 007C.007C.007C (||| in KadmosU: EC3B)
# ⊗ stanza end 2297
# H hiatus <superscript>0048 (superscript ‘H’)
# ∫ dovetail 222B
# ~ responsion 007E
# ¨ anaclasis 00A8 ́
# ictus 0301 ͡
# bridge 0361
# ⏗ metrical triseme 23D7
# ⏘ metrical tetraseme 23D8
# ⏙ metrical pentaseme 23D9