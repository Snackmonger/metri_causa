Hexameter Automaton Notes
=========================

Although I'm well familiar with the hexameter and matters of ancient Greek philology,
I'm a relative newcomer to the world of computer programming. This page is a collection
of notes I used when thinking about how to write the part of the program that will analyze
hexameter. In fact, the sources I used have already solved the problem pretty effectively,
but I wanted to use the process as a way to understand finite automata better myself. 

Bibliography
++++++++++++

RANKER
    Ranker, Hope. (2012) "hexameter" (Finite state automaton for analyzing hexameter). https://github.com/epilanthanomai/hexameter/blob/master/hexameter.py
SCHUMANN
    Schumann, Anne-Kathrin, Christoph Beierle, Norbert Blößner. (year). "Using finite-state machines to automatically scan Ancient Greek hexameter". Digital Scholarship in the Humanities 37(1), pp.242-253. https://github.com/anetschka/greek_scansion/tree/master
WEST-2
    West, M.L. (2018). "Unmetrical Verses in Homer," in *Language and Meter*. Leiden: Brill.


Considerations
++++++++++++++

FINITE STATE PRINCIPLE
----------------------
Regardless of correption, synizesis, muta-cum-liquida, etc., all hexameters must
be resolvable to 32 end-states, organized below by number of spondees

(D stands for the dactly +--, S stands for the spondee ++, X for the 6th foot +- or ++)

::

    0       1       2       3       4       5
    DDDDDX  SDDDDX  SSDDDX  DDSSSX  SSSSDX  SSSSSX
            DSDDDX  DSSDDX  SDDSSX  DSSSSX
            DDSDDX  DDSSDX  SSDDSX  SDSSSX
            DDDSDX  DDDSSX  SSSDDX  SSDSSX
            DDDDSX  SDSDDX  DSDSSX  SSSSDX
                    SDDSDX  DSSDSX
                    SDDDSX  DSSSSX
                    DSDSDX  SDSDSX
                    DDSDSX  SSDSDX
                    DSDDSX  SDSSDX

ARBITRARY LENGTHENING PRINCIPLE
-------------------------------

Words that do not adhere the necessary pattern are sometimes given 
vowel quantities that cannot be justified etymologically. When vowels
that are naturally short are lengthened, they are usually re-spelled to 
reflect the change, but ambiguous vowels simply imply a long quantity.
We will observe that arbitrary lengthenings tend to take place in 
the princeps of the foot, but especially in the first foot and
before a caesura::

        ἀποδίωμαι becomes   αποδῑωμαι
        κῠανόπεπλος         κῡανόπεπλος
        γενόμενον           γεινόμενον
        ὑπὲρ ἅλα            ὑπεὶρ ἅλα
        ἐν ἀγορῆι           εἰν ἀγορῆι
        διογενής            δῑογενής
        Πολυδάμας           Πουλυδάμας
        ἀνέρες, ὕδατι       ανέρες, υδατι (long alpha)
        ὄρεα, ὄρεσι         οὔρεα, οὔρεσι
        ὄνομα               οὔνομα
        ἀθάνατος            αθάνατος (long alpha)
        ἀνεμόεις            ἠνεμόεις
        ζεφυρίη             ζɛ̄φυρίη (Od. 7. 119) (NB not ει)
        κατα(λ)λοφάδια      κατα(λ)λοφάδῑα (Od. 10. 169)
        ἐπίτονος            ɛ̄̓πίτονος (Od. 12. 243) (NB not ει)
        συβόσια             συβόσῑα (Od. 14. 101)

IRREGULAR STRUCTURE PRINCIPLE
-----------------------------
Some hexameters exhibit an irregular structure that cannot be resolved or
explained in a satisfactory way. Perhaps some of these reflect remnants of 
an early form of the hexameter in which syllable structures were looser,
while others may be down to (in some cases very early) textual corruption.

(D here stands for the hemiepes +--+--+)

The form D - D +, as if the second hemistich was meant to follow a feminine caesura::

    Λ 697       εἵλετο κρινάμενος τριηκόσι’ ἠδὲ νομῆας
                +--    +--+       -+--      +-   -++    

                    

The form D - + D +, as if the second hemistich was meant to follow a masculing caesura::

    Il. 4.202   λαῶν, οἵ οἱ ἕποντο Τρίκης ἐξ ἱπποβότοιο
                ++    +  -  -+-    ++    +  +--+-  
    Il. 9.414   εἰ δέ κεν οἴκαδ᾽ ἵκωμαι φίλην ἐς πατρίδα γαῖαν
                +  -  -   +-     -++    -+    +  +--     +-
    Od. 7.89    ἀργύρεοι δὲ σταθμοὶ ἐν χαλκέῳ ἕστασαν οὐδῷ, 
                +--+      +   +-    +   +--   +--     ++

                    Editors emend:
                    σταθμοὶ δ’ ἀργύρεοι ἐν χαλκέῳ ἕστασαν οὐδῷ,
                    ++         +--+     +  +--    +--      ++

                    However, SEDES shows that σταθμοὶ is 3x more common in
                    position 4 than 1. So, if the hiatus were acceptable,
                    we might prefer:
                    ἀργύρεοι σταθμοὶ ἐν χαλκέῳ ἕστασαν οὐδῷ,
                    +--+     ++      +  +--    +--     ++

Something unmetrical::

    Od. 13.194  τοὔνεκ᾿ ἄρ᾿ ἀλλοειδέα φαινέσκετο πάντα ἄνακτι
                +-      -   +-+--      ++--       +-   -+-

                    - ἀλλοειδέα (form and lemma) appear only here; possible solutions
                    have been to take synizesis, or to assume digamma
                    - φαινέσκετο (form) appears only here.

    Il. 18.458  υἱεῖ ἐμῷ ὠκυμόρῳ δόμεν ἀσπίδα καὶ τρυφάλειαν
                +-   -+  +--+    --    +--    +   --+-

                    - perhaps having replaced an earlier υἷι μοι ὠκυμόρῳ (Nauck)
                    on the analogy of υἱεῖ ἐμῷ δόμεναι (Il. 18.144)
        
Anomalous first short syllable::

    διὰ μὲν ἀσπίδος ἦλθε φαεινῆς ὄβριμον ἔγχος (Il. 3. 357).
    ῎Αρες ῎Αρες βροτολοιγέ, μιαιφόνε τειχεσιπλῆτα (Il. 5. 455) .
    Βορέης καὶ Ζέφυρος, τώ τε Θρήικηθεν ἄητον (Il. 9. 5, cf. 23. 195).
    δαΐζων ἵππους τε καὶ ἀνέρας· οὐδέ πω ῞Εκτωρ (Il. 11. 497).
    τὰ περὶ καλὰ ῥέεθρα ἅλις ποταμοῖο πεφύκει (Il. 21. 352).
    λύτο δ᾽ ἀγών, λαοὶ δὲ θοὰς ἐπὶ νῆας ἕκαστοι (Il. 24. 1; some mss. λῦτο).

Thus also lines beginning ἐπεὶ δή (6x), ἴομεν (5x), κλῦθι or κλῦτε (18x, accented as if long, 
but etymologically short).

Anomalous first foot::

    Il. 17.734     πρόσσω ἀΐξας περὶ νεκροῦ δηριάασθαι 
    (no correption where it would normally be expected)

    Il. 12.212     ἐσθλὰ φραζομένωι, ἐπεὶ οὐδὲ μὲν οὐδὲ ἔοικεν 
    (muta cum liquida in following world lengthens open short vowel in biceps, normally only in princeps).
    
    Il. 17. 142    ῞Εκτορ, εἶδος ἄριστε, μάχης ἄρα πολλὸν ἐδεύεο
    (digamma makes position in the biceps, normally only in the princeps)

    Il. 21. 368     πολλὰ λισσόμενος ἔπεα πτερόεντα προσηύδα
    (initial resonant lengthens in the biceps, normally only in the princeps)

    Ps-Hes. fr.204.41  μνᾶτο· πλεῖστα δὲ δῶρα μετὰ ξανθὸν Μενέλαον
    Ps-Hes. fr.204.54  μνᾶτο· πολλὰ δὲ δῶρα δίδου, μάλα δ᾽ ἤθελε θυ[μῶι,
    Ps-Hes. fr.199.3   εἶδος οὔ τι ἰδών, ἀλλ᾽ ἄλλων μῦθον ἀκούων.

Some lines have defective endings, perhaps reflecting alternate syllabifications
of a proto-form::

    Il. 12.208      Τρῶες δ’ ἐρρίγησαν ὅπως ἴδον αἰόλον ὄφιν
                    ++       +++-      -+   --   +--    --

MISSING CONSONANT PRINCIPLE
---------------------------
In some cases, vowels were lengthened by a consonant that is now lost, 
as in the case of words originally containing digamma, and words beginning with a
sibilant + resonant

Lost digamma::

    Il. 13.573      ὣς ὃ τυπεὶς ἤσπαιρε μίνυνθά περ, οὔ τι μάλα δήν
                    +  - -+     ++-     -+-     -    +  -  --   +
                    ὣς ὃ τυπεὶς ἤσπαιρε μίνυνθά περ, οὔ τι μάλα δϝήν
                    +  - -+     ++-     -+-     -    +  -  -+   +

Lost sigma::

    Il. 12. 278     τῶν δ᾽ ὥς τε νιφάδες χιόνος πίπτωσι θαμειαί
                    +      +  -  --+     --+    ++-     --+
                    τῶν δ᾽ ὥς τε σνιφάδες χιόνος πίπτωσι θαμειαί
                    +      +  +  --+      --+    ++-     --+

    Il. 16. 143     Πηλιάδα μελίην, τὴν πατρὶ φίλωι πόρε Χείρων
                    +---    --+     +   +-    -+    --   ++
                    Πηλιάδα σμελίην, τὴν πατρὶ φίλωι πόρε Χείρων
                    +---    --+      +   +-    -+    --   ++

Lost sigma and digamma together::

    Il. 3. 172      αἰδοῖός τέ μοί ἐσσι, φίλε ἑκυρέ, δεινός τε
                    +++     -  -   +-    --   ---    ++     -
                    αἰδοῖός τέ μοί ἐσσι, φίλε σϝεκυρέ, δϝεινός τε.
                    +++     -  -   +-    -+   --+      ++      -

    Il. 5. 343      ἣ δὲ μέγα ἰάχουσα ἀπὸ ἕο κάββαλεν υἱόν
                    + -  -  - --+-    --  -- +--      +-
                    ἃ δὲ μέγα ϝιϝάχονσα ἀπὸ σϝέο κάββαλεν υἱόν.
                    + -  -  - --+-      -+  --   +--      +-
                    (the alpha of μέγα is arbitrarily long in any case)

However, this principle is also applied analogically in places where it is
not eymologically appropriate::
    
    Od. 1. 269      οἷσιν ἐνὶ μεγάροισι· σὲ δὲ φράζεσθαι ἄνωγα
                    +-    --  --+-       -  +  ++-       -+-
                    (as if σμεγάροισι)

    Il. 17. 595     ἀστράψας δὲ μάλα μεγάλ᾽ ἔκτυπε, τὴν δὲ τίναξε
                    +++      -  --   --     +--     +   -  -+-
                    (as if σμεγάλ᾽)

ADAPTED FORMULA PRINCIPLE
-------------------------
Some of these metrical abberations may be the result of fomulaic transposition, in 
which a formula expecting a vowel/consonant is used in a new context with the wrong
sequel, or in which a formula is displaced into an unexpected sedes::

    Od. 10.87       ἔνθ’ ἐπεὶ ἐς λιμένα κλυτόν 
                    +    --   +  --+    --
    Od. 10.141      ναύλοχον ἐς λιμένα, καί τις θεὸς ἡγεμόνευεν
                    +--      +  ---     +   +   --   +--+-

    Il. 24.104      ἤλυθες Οὔλυμπόνδε θεὰ Θέτι κηδομένη περ
    Il. 18. 385     τίπτε, Θέτι τανύπεπλε, ἱκάνεις ἡμέτερον δῶ; 

    (Though explained by later sources as contracted from Θέτιϊ)
    
The vocative is especially prone to this phenomenon::

    Od. x27         Τηλέμαχ’ + vowel
    Od. x3          Τηλέμαχε + double consonant
    Od. 3.230       Τηλέμαχε, ποῖόν σε ἔπος φύγεν ἕρκος ὀδόντων
                    +---      ++    -  -+   --    +-    -++

    Il. 21.308      φίλε κασίγνητε, σθένος ἀνέρος ἀμφότεροί περ
                    +-   -+++       --     +--    +--+      -
    Il. 4. 155      φίλε κασίγνητε, θάνατόν νύ τοι ὅρκι᾽ ἔταμνον
                    +-   -++-       --+     -   -  +-    -+-
    Il. 5. 359      φίλε κασίγνητε, κόμισαί τέ με δός τέ μοι ἵππους 
                    +-   -++-       --+     -  -  +   -  -   ++

And this occurs not only when a single form is transposed, but also when a formula 
is adapted to accommodate the vocative::

    Il. 2.6         πέμψαι ἐπ’ Ἀτρεΐδῃ Ἀγαμέμνονι οὖλον ὄνειρον· 
                                                  +-    -+-
    Il. 2.8         βάσκ᾽ ἴθι, οὖλε ῎Ονειρε, θοὰς ἐπὶ νῆας ᾽Αχαιῶν
                               +-    -+-                   

    Il. 4.327       εὗρ’ υἱὸν Πετεῶο Μενεσθῆα πλήξιππον 
                    +    ++   --+-
    Il. 4. 338      ὦ υἱὲ Πετεῶιο διοτρεφέος βασιλῆος 
                    + +-  --+-

    Il. 1. 551      Τὸν δ’ ἠμείβετ’ ἔπειτα βοῶπις πότνια Ἥρη·
                                           -++    +--    ++
    Il. 8. 471      ὄψεαι, αἴ κ᾽ ἐθέληισθα, βοῶπι πότνια ῞Ηρη
                                            -+-   +--     ++

    Il. 16. 149     Ξάνθον καὶ Βαλίαν, τὼ ἅμα πνοιῇσι πετέσθην,
                    ++     +   --+
    Il. 19. 400     Ξάνθέ τε καὶ Βαλίε, τηλεκλυτὰ τέκνα Ποδάργας
                    +-    -  +   --+

    νηπύτιε, τί νυ τόξον ἔχεις ἀνεμώλιον αὔτως; (21. 474, cf. 410, 441).

And in some cases, this applies to cases aside from the vocative::
                                                
    Il. 18.288      πρὶν μὲν γὰρ Πριάμοιο πόλιν μέροπες ἄνθρωποι
                    +    +   +   --+-     -+    ---     +++
                                                μερόπων ἀνθρώπων (7x)
                                                --+    +++

MISSING VOWEL PRINCIPLE
-----------------------
In the Indo-European language, resonant segments were treated as vowels when
they were surrounded by less sonorant segments. A similar treatment of rho in
Greek has been offered as a solution to certain unmetrical hexameters. That is,
in a previous phase of the language, the rho in these lines functioned as a vowel,
but was re-syllabified in the later language as groups of consonant + vowel, 
creating lines that no longer scan properly::

    Μηριόνης (τ’) ἀτάλαντος Ἐνῡαλίῳ ἀνδρειφόντῃ (Il. 2.651; 7.166; 8.264; 17.259)
    +--+          --+-      -+--+   ++++
    ὃν πότμον γοόωσα, λιποῦσ᾽ ἀνδροτῆτα καὶ ἥβην (Il. 16. 857).
    Πατρόκλου ποθέων ἀνδροτῆτά τε καὶ μένος ἠΰ (Il. 24. 6).
    αὖθι μένειν, μή πως ἀβροτάξομεν ἀλλήλοιϊν (Il. 10. 65),
    νὺξ ἀβρότη, ἢν καὶ τῆι ἀπόσχωνται πολέμοιο (Il. 14. 78),

In its proto-form, the rho serves as a short vowel and scans properly::

    Μηριόνης (τ’) ἀτάλαντος Ἐνῡαλίῳ ἀνρφόντῃ
    +--+          --+-      -+--+   --++

TRANSFERRED QUANTITY PRINCIPLE
------------------------------
One of the phonological changes that the Greek language underwent over time 
involved the transfer of quantities in adjacent vowels, causing previously
metrical verses to become unmetrical::

    ἕως ὃ ταῦθ᾽ ὥρμαινε κατὰ φρένα καὶ κατὰ θυμόν (Il. 1. 193 et al.)
    βὰν δ᾽ ἰέναι προτέρω διὰ δώματος, ἕως ἵκοντο (Od. 15. 109)

    In which ἕως has undergone a tranfer of quantity from earlier ἧος.

    

8. Similarly, inflections with contracted syllables might be scanned as if 
uncontracted.
    ᾽Ιλίου προπάροιθεν          (Il. 15. 66, 22. 6)
    +-+    --+-
    for the uncontracted
    ᾽Ιλίοο προπάροιθεν
    +--+   --+-

    βῆν εἰς Αἰόλου κλυτὰ δώματα (Od. 10. 60, cf. 36)
    +   +   +-+    --    +--
    for the uncontracted
    βῆν εἰς Αἰόλοο κλυτὰ δώματα 
    +   +   +--+   --    +--

9. Some abberations may represent textual corruptions that entered the tradition
early enough to have become the new standard. 

    

WELL-FORMED VERSES
------------------

There is a preference for a dactylic fifth foot, especially when the line
ends with a disyllabic word, with the ending ++++ being very uncommon. When 
it does occur, it is nearly always clear that the long biceps in the fifth 
foot is the product of vowel contraction::

    ἤ πού τίς σφιν ἔνισπε θεοπροπέων εὖ εἰδώς (Il. 6. 438, < *ἔϋ).
    ἐγγύθεν ᾽Αρήνης, ὅθι μείναμεν ἠῶ δῖαν (Il. 11. 723, < *ἠόα).
    ἦεν ἀνήνασθαι, χαλεπὴ δ᾽ ἔχε δήμου φῆμις (Od. 14. 239, < *δήμοο).
    οἴνωι Πραμνείωι, ἐπὶ δ᾽ αἴγειον κνῆ τυρόν (Il. 11. 639, < *κνάε?).
    ἀμφὶ δ᾽ ἄρ᾽ αἰγείρων ὑδατοτρεφέων ἦν ἄλσος (Od. 17. 208, < *ἔεν?).

But contraction also justifies monosyllables of other types, and we find::

    πυροί τε ζειαί τε ἰδ᾽ εὐρυφυὲς κρῖ λευκόν (Od. 4. 604).
    ἀλλά τε καὶ τῶν αἰὲν ἀφαιρεῖται λὶς πέτρη (Od. 12. 64).
    HDem.204    μειδῆσαι γελάσαι τε καὶ ἵλαον σχεῖν θυμόν


"""