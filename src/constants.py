"""Constants used in the program."""
from enum import StrEnum, auto

ALPHA_VARIANTS = "ἀἁἂἃἄἅἆἇἈἉἊἋἌἍἎἏὰάᾀᾁᾂᾃᾄᾅᾆᾇᾈᾉᾊᾋᾌᾍᾎᾏᾰᾱᾲᾳᾴᾶᾷᾸᾹᾺΆᾼαΑόά"
EPSILON_VARIANTS = "ἐἑἒἓἔἕἘἙἚἛἜἝὲέεΕέ"
ETA_VARIANTS = "ἠἡἢἣἥἤἦἧἨἩἪἫἬἭἮἯὴήᾐᾑᾒᾓᾔᾕᾖᾗᾘᾙᾚᾛᾜᾝᾞᾟῂῃῄῆῇῈΈῊΉῌηΗή"
IOTA_VARIANTS = "ἰἱἲἳἴἵἶἷἸἹἺἻἼἽἾἿὶίῐῑῒΐῖῗῘῙῚΊιΙίϊΐ"
OMICRON_VARIANTS = "ὀὁὂὃὄὅὈὉὊὋὌὍὸόόοΟ"
UPSILON_VARIANTS = "ὐὑὒὓὔὕὖὗὙὛὝὟὺύῦῧῨῩῪΎῠῡῢΰυύΥΰ"
OMEGA_VARIANTS = "ὠὡὢὣὤὥὦὧὨὩὪὫὬὭὮὯὼώᾠᾡᾢᾣᾤᾥᾦᾧᾨᾩᾪᾫᾬᾭᾮᾯῲῳῴῶῷῸΌῺΏῼωΩώ"
ELISION = "’"
VOWELS = ALPHA_VARIANTS + EPSILON_VARIANTS + IOTA_VARIANTS + OMICRON_VARIANTS \
    + OMEGA_VARIANTS + UPSILON_VARIANTS + ETA_VARIANTS + ELISION
LONG_VOWELS = ETA_VARIANTS + OMEGA_VARIANTS
SHORT_VOWELS = EPSILON_VARIANTS + OMICRON_VARIANTS
AMBIGUOUS_VOWELS = UPSILON_VARIANTS + IOTA_VARIANTS + ALPHA_VARIANTS
STOPS = "ΒΓΔΘΚΠΣΤΦΧβγδθκπστφχ"
RESONANTS = "λΛμΜνΝρΡ"
RHO_VARIANTS = "ῤῥῬρ"
SIGMA_VARIANTS = "σΣς"
DOUBLE_CONSONANTS = "ζψξΖΨΞ"
PUNCTUATION = "«».,·;"
CONSONANTS = STOPS + RESONANTS + RHO_VARIANTS + SIGMA_VARIANTS + DOUBLE_CONSONANTS

class Scansion(StrEnum):
    """Types of vowel length."""
    LONG = auto()
    SHORT = auto()
    AMBIGUOUS = auto()
    LONG_MUTABLE = auto()
    SHORT_MUTABLE = auto()
    AMBIGUOUS_MUTABLE = auto()
