Greek Metrical Analysis Tool 
============================

.. contents:: 

Version 0.1.2, May 9 2024
------------------------
Elision
    Elisions are now handled correctly. Elisions are marked as a 'vowel' so that the
    parser is able to contextualize them in words, and it is up to the interpreter
    to treat them as null syllables. We may encounter some problems in deciding 
    which colon null monosyllables are supposed to go with::

        Φῆ πυρὶ καιόμενος, ἀνὰ | δ’ ἔφλυε καλὰ ῥέεθρα.
        Φῆ πυρὶ καιόμενος, ἀνὰ δ’ | ἔφλυε καλὰ ῥέεθρα.

    Off the top of my head, elided monosyllables will be ge, te, de, ke, me, se, all 
    of which are postpositives or enclitics, so the pause should come after these words.
Next Steps
    Start working on scanning hexameter. We will read the following paper and try 
    to implement its automaton:

    Schumann, A-K., et al. (2022). "Using Finite-State Machines to Automatically Scan 
    Ancient Greek Hexameter", in *Digital Scholarship in the Humanities*, Vol. 37. No. 1.

Sample Analysis
    Now elisions are marked with "E"::

        -       0            1        2    3     4          5        6           7
        0  [+, E]    [-, ?, +]  [+*, +]  [-]  [+*]  [+, ?, ?]  [+*, -]   [?, +, +]
        1   λῆγ.’  ἔ.ρι.δος[,]   Τρῶ.ας   δὲ   καὶ   αὐ.τί.κα    δῖ.ος  Ἀ.χιλ.λεὺς
                    0                  1    2     3          4     5            6
        0  [+, -*, -]   [+, -, ?, +*, -]  [?]  [+*]  [-, ?, +]  [+*]    [?, +, +]
        1    ἄσ.τε.ος  ἐκ.σε.λά.σει.ε[·]   τί   μοι   ἔ.ρι.δος   καὶ  ἀ.ρω.γῆς[;]
             0       1                2       3    4           5       6            7
        0  [+]  [?, ?]    [+*, -, -, -]  [?, ?]  [E]  [M, ?*, -]  [?, ?]   [-*, M, ?]
        1   Φῆ   πυ.ρὶ  και.ό.με.νος[,]    ἀ.νὰ   δ’     ἔφ.λυ.ε   κα.λὰ  ῥέ.εθ.ρα[.]
             0    1       2     3       4                5       6       7
        0  [+]  [-]  [-, +]  [+*]  [+, -]  [-, +, -, -, +]  [?, ?]  [+, +]
        1   ὡς   δὲ  λέ.βης  σδεῖ  ἔν.δον  ἐ.πει.γό.με.νος   πυ.ρὶ  πολ.λῷ
                 0              1                    2               3
        0   [?, +]   [+, -, -, -]  [?, ?, M, -, -*, +]  [?*, ?, +*, -]
        1  κνί.σην  μελ.δό.με.νος    ἁ.πα.λοτ.ρε.φέ.ος      σι.ά.λοι.ο
                    0                1       2    3       4          5           6
        0   [+, -, -]     [+, -, ?, +]  [?, -]  [+]  [?, ?]  [+, ?, ?]      [+, +]
        1  πάν.το.θεν  ἀμ.βο.λά.δην[,]    ὑ.πὸ   δὲ  κσύ.λα  κάγ.κα.να  κεῖ.ται[,]
             0    1       2           3       4             5        6    7         8
        0  [+]  [+]  [?, ?]  [-*, M, ?]  [?, M]     [-, -, +]  [-*, -]  [E]    [?, +]
        1   ὣς  τοῦ   κα.λὰ    ῥέ.εθ.ρα   πυ.ρὶ  φλέ.γε.το[,]    σδέ.ε   δ’  ὕ.δωρ[·]
                0          1              2       3            4       5    6           7
        0  [+, E]  [-, -, M]     [-, -*, +]  [+, E]    [+, -, -]  [+, -]  [E]  [?*, M, +]
        1   οὐδ.’    ἔ.θε.λε  προ.ρέ.ειν[,]   ἀλλ.’  ἴσ.χε.το[·]  τεῖ.ρε   δ’     ἀ.ϋτ.μὴ
                       0           1                 2       3    4    5       6
        0  [+, +, +*, -]  [?*, +, ?]      [-, M, -, -]  [+, ?]  [-]  [E]  [+, +]
        1   Ἡ.φαίσ.τοι.ο     βί.η.φι  πο.λύφ.ρο.νος[.]  αὐ.τὰρ    ὅ   γ’   Ἥ.ρην
                0              1           2              3              4
        0  [+, ?]   [+, -, -, -]  [-, -*, +]  [-, -*, +, M]      [-, +, ?]
        1  πολ.λὰ  λισ.σό.με.νος      ἔ.πε.α   πτε.ρό.εν.τα  προ.σηύ.δα[·]

Version 0.1.1, May 07 2024
-------------------------
Abstract
    The program is meant to aid in the analysis and composition of Greek poetry.
    On the one hand, it should be able to parse the syllable structure of Greek poetry
    into metrical cola, but it should also be able to analyse the adherance of those
    cola to given metrical constraints (trimeter and hexameter mostly). It should be
    able to search a corpus of poetry to find cola that will fit a requested pattern.

    The program follows a very simple compiler/interpreter architecture.

Tokenizer
    The lexical grammar sorts alphabetic glyphs into different token classes.
    The tokenizer attempts to consider the presence of diacritical marks to 
    determine whether adjacent vowels should be tokenized as diphthongs. 
    Consonants are sorted into basic articulation types: stop, resonant,
    sibilant, double. Whitespace is converted into word-end and word-beginning
    tokens. Newlines and line breaks ("-") are used as cues to interpreting the
    intended metrical cola.

Parser
    The parser creates a simple syntax tree representing the syllabic structure
    of the lines it receives. 
    
    During parsing, any digraph consonant (xi, psi, zeta) is broken down into 
    its constituents, so that a syllable boundary can be placed between them.

    A punctuation mark is incorporated as an annotation in the 'word' nodes.

Basic Interpreter
    The interpreter checks each node for any relevant information, and passes 
    it up the tree to where it will be useful. Any closed syllable within a 
    word is long, but may be muta-cum-liquida. Any open syllable will have its
    surface-vowel length, but may be marked as mutable if it is followed by 
    another vowel. A syllable at the end of a word may disguise a hidden
    length. A word ending with a short open vowel may be closed by consonants at
    the beginning of the next word. A word ending in a closed short vowel may be
    syllabified as open if the next word begins with a vowel.

Pending Features
    - In the next version of the program, we will introduce an interpreter specific
    to hexameter texts, that will attempt to resolve ambiguous vowels into proper
    quantities, and identify deviations from hexameter "laws".
    
    - In the future, I should also like to support analysis of elegiac distichs.

Sample Analysis
    This is an example of the current state of the program. It analyses 
    scansion, but does not attempt to resolve ambiguities within any specific
    metrical scheme. 

    - Certainly long vowels are indicated with "+"
    - Certainly short vowels are indicated with "-"
    - Ambiguous vowels are indicated with "?"
    - Mutable vowels are indicated with "*"
    - Short/ambiguous muta cum liquida are indicated with "M"
    
    Nonnus, Dionysiaka 1.1-45::

        -         0        1              2              3          4          5
        0    [+, -]  [-*, M]  [-, ?, ?*, -]  [?*, +, -, -]  [+, -, -]     [+, +]
        1  εἰ.πέ[,]  θε.ά[,]    Κρο.νί.δα.ο   δι.άκ.το.ρον  αἴ.θο.πος  αὐ.γῆς[,]

                    0           1              2       3              4
        0  [+, ?, ?*, +]   [+, +, ?]   [-, +, -, -]  [+, ?]      [-, +, +]
        1    νυμ.φι.δί.ῳ  σπιν.θῆ.ρι  μο.γοσ.τό.κον  ἄσ.θμα  κε.ραυ.νοῦ[,]

            0           1          2                   3       4    5        6
        0  [+]   [-, -, +]  [-, -, +]     [?, ?, +, -, -]  [+, -]  [-]   [M, +]
        1  καὶ  στε.ρο.πὴν  Σε.μέ.λης  θα.λα.μη.πό.λον[·]   εἰ.πὲ   δὲ  φύτ.λην

                0                   1    2    3       4       5           6
        0   [+, +]    [+, -, -, +*, -]  [-]  [+]  [?, -]  [M, -]  [?*, +, +]
        1  Βάκ.χου  δισ.σο.τό.κοι.ο[,]  τὸν   ἐκ  πυ.ρὸς  ὑγ.ρὸν    ἀ.εί.ρας

            0        1                2                  3              4
        0    [+]   [-, -]  [+, ?, -, +, -]  [?, +*, +, +*, -]      [-, +, +]
        1  ΣΔεὺς  βρέ.φος  ἡ.μι.τέ.λεσ.τον     ἀ.μαι.εύ.τοι.ο  τε.κού.σης[,]

                        0             1       2           3              4
        0    [+, -, -, +]  [?, ?, +, ?]  [-, +]  [+, +*, -]      [?, +, +]
        1  φει.δο.μέ.ναις   πα.λά.μῃ.σι  το.μὴν    μη.ροῖ.ο  χα.ράκ.σας[,]

                0        1             2       3    4           5          6
        0  [+, -, ?]   [+, ?]     [-, +, -]  [?, +]  [+]  [M, ?*, ?]     [+, +]
        1   ἄρ.σε.νι  γασ.τρὶ  λό.χευ.σε[,]  πα.τὴρ  καὶ    πότ.νι.α  μή.τηρ[,]

            0       1       2          3       4              5            6
        0  [+*]  [+, +]  [-, -]     [+, -]  [-, +]  [-, -*, +, ?]    [?, +, +]
        1    εὖ  εἰ.δὼς  τό.κον  ἄλ.λον[,]   ἐ.πεὶ    γο.νό.εν.τι  κα.ρή.νῳ[,]

                0       1          2       3             4          5
        0  [+, -, -]  [+, -]  [?, +, -]  [-, +]  [+, ?, -, ?]     [+, +]
        1  ἄσ.πο.ρον  ὄγ.κον  ἄ.πισ.τον   ἔ.χων   ἐγ.κύ.μο.νι  κόρ.σῃ[,]

                    0                1                 2            3
        0   [+, -, ?]     [+, +, +, ?]   [?, +, +, +, -]    [?, +, +]
        1  τεύ.χε.σιν  ἀσ.τράπ.του.σαν  ἀ.νη.κόν.τισ.δεν  Ἀ.θή.νην[.]

                0    1             2             3             4           5
        0  [+, ?, -]  [+]     [+, +, ?]  [?, +, ?, -]     [+, ?, ?]      [+, +]
        1   ἄκ.σα.τέ  μοι  νάρ.θη.κα[,]  τι.νάκ.σα.τε  κύμ.βα.λα[,]  Μοῦ.σαι[,]

            0          1       2        3                 4               5
        0  [+]  [?, ?, +]  [-, -]   [+, -]  [?*, +, -, -, +]   [?*, -, ?, +]
        1  καὶ   πα.λά.μῃ   δό.τε  θύρ.σον    ἀ.ει.δο.μέ.νου  Δι.ο.νύ.σου[·]

                0       1              2       3       4          5         6
        0  [+, ?]  [-, +]     [+*, +, ?]  [?, +]  [?, ?]  [+, -, ?]    [+, +]
        1   ἀλ.λὰ  χο.ροῦ  πσαύ.ον.τα[,]   Φά.ρῳ   πα.ρὰ  γεί.το.νι  νή.σῳ[,]

                0    1           2                 3       4           5
        0  [+, ?, -]  [M]  [+, +*, ?]      [-, M, -, -]  [M, ?]  [?, +*, +]
        1  στή.σα.τέ  μοι    Πρω.τῆ.α  πο.λύτ.ρο.πον[,]   ὄφ.ρα    φα.νεί.η

                    0       1         2       3           4       5            6
        0   [+, ?, -]  [+, -]    [-, +]  [-, ?]   [+, ?, -]  [+, -]    [?, +, +]
        1  ποι.κί.λον  εἶ.δος  ἔ.χων[,]    ὅ.τι  ποι.κί.λον  ὕμ.νον  ἀ.ράσ.σω[·]

            0    1                 2        3               4         5
        0  [+]  [?]  [-, +, +, +*, M]   [?, +]    [M, +, -, -]    [+, +]
        1   εἰ  γὰρ   ἐ.φερ.πύσ.σει.ε  δρά.κων  κυκ.λού.με.νος  ὁλ.κῷ[,]

                0        1            2       3              4       5
        0   [+, +]  [+*, -]   [?*, M, -]  [-, +]  [+, +, -*, ?]  [+, +]
        1  μέλ.πσω   θεῖ.ον  ἄ.εθ.λον[,]   ὅ.πως    κισ.σώ.δε.ϊ  θύρ.σῳ

                0                  1                 2       3              4
        0   [+, M]    [?, +, -, -, +]  [-, ?*, +, -, -]  [?, ?]      [?, +, +]
        1  φρικ.τὰ  δρα.κον.το.κό.μων     ἐ.δα.ΐσ.δε.το   φῦ.λα  Γι.γάν.των[·]

            0    1        2            3                 4       5          6
        0  [+]  [-]  [-*, +]   [+, +*, -]  [-, +, -, ?*, +]  [?, ?]    [+*, +]
        1   εἰ   δὲ    λέ.ων  φρίκ.σει.εν    ἐ.παυ.χε.νί.ην  τρί.χα  σεί.ων[,]

                0              1           2       3           4        5
        0   [+, -]  [?, +*, +, +]   [-, ?, +]  [-, ?]  [+, -*, ?]  [+*, +]
        1  Βάκ.χον    ἀ.νευ.άκ.σω  βλο.συ.ρῆς    ἐ.πὶ     πή.χε.ϊ   Ῥεί.ης

                0                 1                     2             3
        0   [+, -]   [?, M, +, +, ?]  [-*, +, -, -, +*, -]    [-*, +, +]
        1  μασ.δὸν  ὑ.ποκ.λέπ.τον.τα     λε.ον.το.βό.τοι.ο  θε.αί.νης[·]

            0    1                  2              3          4        5
        0  [+]  [-]  [?*, +, +*, +, ?]  [-, +, ?*, -]  [+, ?, ?]   [+, +]
        1   εἰ   δὲ     θυ.ελ.λή.εν.τι   με.τάρ.σι.ος   ἅλ.μα.τι  ταρ.σῶν

                    0           1                 2       3             4
        0   [+, ?, ?]  [?*, +, +]   [-, ?, +, ?, -]  [+, -]     [?, +, +]
        1  πόρ.δα.λις     ἀ.ίκ.σῃ  πο.λυ.δαί.δα.λον  εἶ.δος  ἀ.μεί.βων[,]

                0        1        2       3       4          5       6
        0  [+, +, +]  [?*, -]  [+*, ?]  [-, +]  [-, -]  [+, ?, -]  [+, +]
        1   ὑμ.νή.σω    Δι.ὸς  υἷ.α[,]  πό.θεν  γέ.νος  ἔκ.τα.νεν  Ἰν.δῶν

                    0              1               2                3
        0  [+, ?, ?*, +]  [-, -*, +, ?]    [?, +, +, ?]     [-, -, +, +]
        1   πορ.δα.λί.ων     ὀ.χέ.εσ.σι  κα.θιπ.πεύ.σας  ἐ.λε.φάν.των[·]

            0       1             2       3         4        5           6
        0  [+]  [-, ?]  [?, +, +, -]  [?, +]   [?*, -]  [+*, ?]  [?*, +, +]
        1   εἰ  δέ.μας  ἰ.σάσ.δοι.το   τύ.πῳ  συ.ός[,]     υἷ.α    Θυ.ώ.νης

                    0              1              2          3          4
        0  [?*, +, +]  [-, -*, +, ?]  [?*, +, -, -]  [+, ?, -]     [+, +]
        1     ἀ.εί.σω    πο.θέ.ον.τα   συ.οκ.τό.νον  εὔ.γα.μον  Αὔ.ρην[,]

                    0              1             2          3           4
        0  [+, ?, -, M]  [?, ?, +*, -]  [?, +, ?, ?]  [+, -, ?]      [+, +]
        1  ὀπ.σι.γό.νου   τρι.τά.τοι.ο   Κυ.βη.λί.δα   μη.τέ.ρα  Βάκ.χου[·]

            0    1       2          3         4              5           6
        0  [+]  [-]  [-, +]  [?, +, -]    [?, +]  [?*, -, ?, -]  [?*, +, +]
        1   εἰ   δὲ  πέ.λοι  μι.μη.λὸν  ὕ.δωρ[,]    Δι.ό.νυ.σον     ἀ.εί.σω

                0       1          2                    3               4
        0   [+, -]  [?, +]  [?, +, ?]  [-, +, -, -, +*, -]       [?, +, +]
        1  κόλ.πον   ἁ.λὸς  δύ.νον.τα   κο.ρυσ.σο.μέ.νοι.ο  Λυ.κούρ.γου[·]

            0       1              2       3              4              5
        0  [+]  [?, -]   [+, +, +, -]  [-, +]   [?, ?, M, ?]      [?, +, +]
        1   εἰ  φυ.τὸν  αἰ.θύσ.σοι.το  νό.θον  πσι.θύ.ρισ.μα  τι.ταί.νων[,]

                    0                  1       2       3           4       5
        0  [+, -, +*]  [?, ?, ?*, +*, -]  [-, +]  [?, ?]  [+*, ?, ?]  [+, +]
        1  μνή.σο.μαι    Ἰ.κα.ρί.οι.ο[,]  πό.θεν   πα.ρὰ    θυι.ά.δι   λη.νῷ

                0                1       2             3          4
        0   [M, ?]  [?, +, +, +, ?]  [-, +]  [M, ?, -, -]     [+, +]
        1  βότ.ρυς   ἁ.μιλ.λη.τῆ.ρι  πο.δῶν   ἐθ.λί.βε.το  ταρ.σῷ[.]

                0    1             2                 3              4    5
        0  [+, ?, -]  [+]     [+, +, ?]      [?, +, -, -]  [+, ?, ?*, +]  [-]
        1   Ἄκ.σα.τέ  μοι  νάρ.θη.κα[,]  Μι.μαλ.λό.νες[,]     ὠ.μα.δί.ην   δὲ

                0                 1             2       3          4
        0  [M, ?, ?]   [+, ?, -, +, -]  [-, +, -, -]  [+, ?]  [?, +, +]
        1  νεβ.ρί.δα  ποι.κι.λό.νω.τον   ἐ.θή.μο.νος   ἀν.τὶ  χι.τῶ.νος

                    0    1               2             3           4       5
        0    [+, ?, -]  [+]       [+, +, ?]  [?, +, ?, -]  [+, -*, -]  [M, +]
        1  σφίγ.κσα.τέ  μοι  στέρ.νοι.σι[,]  Μα.ρω.νί.δος   ἔμ.πλε.ον  ὀδ.μῆς

                        0           1    2    3              4     5          6
        0    [+, ?, -*, +]  [?, ?*, +]  [-]  [?]  [+, -, -*, +]  [+*]  [-, +, +]
        1  νεκ.τα.ρέ.ης[,]     βυ.θί.ῃ   δὲ  παρ     Εἰ.δο.θέ.ῃ   καὶ    Ὁ.μή.ρῳ

                    0       1       2              3              4
        0  [+, ?*, +]  [?, ?]  [+, ?]   [?, +, +, +]  [-, -, ?*, +]
        1    φω.κά.ων   βα.ρὺ  δέρ.μα  φυ.λασ.σέσ.θω  Με.νε.λά.ῳ[.]

                    0    1       2        3     4             5             6    7
        0  [+*, ?*, ?]  [+]  [-, -]   [+, ?]  [+*]     [+, ?, ?]  [+, ?, -, +]  [-]
        1       εὔ.ι.ά  μοι   δό.τε  ῥόπ.τρα   καὶ  αἰ.γί.δας[,]    ἡ.δυ.με.λῆ   δὲ

                0           1       2               3    4     5          6
        0  [+, +]  [M, -*, -]  [+, -]    [-, +, ?, -]  [+]  [+*]  [-, ?, +]
        1   ἄλ.λῳ   δίθ.ρο.ον  αὐ.λὸν  ὀ.πάσ.σα.τε[,]   μὴ   καὶ    ὀ.ρί.νω

                0         1          2    3              4           5        6
        0   [+, -]    [-, +]  [-, ?, +]  [?]  [?, +, -, +*]  [+, -*, -]   [+, +]
        1  Φοῖ.βον  ἐ.μόν[·]  δο.νά.κων  γὰρ   ἀ.ναί.νε.ται   ἔμ.πνο.ον  ἠ.χώ[,]

            0       1               2              3       4           5
        0  [+]  [-, -]  [+, ?*, ?*, -]  [-*, +, ?, -]  [+, -]   [-, +, +]
        1  ἐκσ    ὅ.τε      Μαρ.σύ.α.ο    θε.η.μά.χον  αὐ.λὸν  ἐ.λέγ.κσας

                0                 1       2               3           4
        0  [+, ?]  [?, +*, +, +, -]  [?, +]    [+, +, -, -]      [+, +]
        1  δέρ.μα     πα.ρῃ.ώ.ρη.σε   φυ.τῷ  κολ.πού.με.νον  αὔ.ραις[,]

                    0       1        2                 3            4
        0   [+, +, ?]  [-, ?]  [+*, ?]  [?, +, ?, +*, -]   [-, +*, +]
        1  γυμ.νώ.σας    ὅ.λα    γυῖ.α   λι.πορ.ρί.νοι.ο  νο.μῆ.ος[.]

                0        1           2             3           4           5
        0    [+, ?]  [-*, ?]   [+, +, -]  [?, +, -, -]  [+, -*, -]      [M, +]
        1  ἀλ.λά[,]  θε.ά[,]  μασ.τῆ.ρος   ἀ.λή.μο.νος     ἄρ.χε.ο  Κάδ.μου[.]