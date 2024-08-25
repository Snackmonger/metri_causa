# pylint:disable=missing-class-docstring
import pandas
from src.interpreter import LengthInterpreter
from src.parser import GreekSyllableParser
from src.printer import SyllableTreePrinter
from src.tokenizer import GreekTokenizer
from src.utils import normalize_text, simplify_metrical_symbols


class SyllabificationPrinter:
    """Class that prints a simplified version of the syllable structure
    of a given text.
    """
    def __init__(self, text: str):
        tokens = GreekTokenizer().tokenize(text)
        printer = SyllableTreePrinter()
        lines = GreekSyllableParser().parse(tokens)
        for line in lines:
            print(line.accept(printer))

class LengthTest:
    """Class that prints an ugly version of the scansion of a given passage."""
    def __init__(self, text: str) -> None:
        text = normalize_text(text)
        tokens = GreekTokenizer().tokenize(text)
        interpreter = LengthInterpreter()
        lines = GreekSyllableParser().parse(tokens)
        for line in lines:
            cola = line.accept(interpreter)
            printer = SyllableTreePrinter()
            words = [word.accept(printer) for word in line.words]

            symbols = [simplify_metrical_symbols(x) for x in cola]
            df = pandas.DataFrame([symbols, words])
            # df.style.set_properties(**{"text-align": "left"})
            print(df)
            # line_assessment = count_syllables(cola)
            # line_adherence = sorted([(x, y) for x, y in adherence(cola).items()])
            # print(f"Certain longs: {line_assessment.certain_long}, certain short: {line_assessment.certain_short}, total syllables: {line_assessment.total}")
            # print(f"Adherences: {line_adherence}")
