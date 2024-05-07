# pylint:disable=missing-class-docstring
import pandas
from src.interpreter import LengthInterpreter
from src.parser import GreekSyllableParser
from src.printer import SyllableTreePrinter
from src.tokenizer import GreekTokenizer
from src.utils import simplify_metrical_symbols


class SyllabificationPrinter:
    def __init__(self, text: str):
        tokens = GreekTokenizer().tokenize(text)
        printer = SyllableTreePrinter()
        lines = GreekSyllableParser().parse(tokens)
        for line in lines:
            print(line.accept(printer))


class LengthTest:
    """Class that prints an ugly version of the scansion of a given passage."""
    def __init__(self, text: str) -> None:
        tokens = GreekTokenizer().tokenize(text)
        interpreter = LengthInterpreter()
        lines = GreekSyllableParser().parse(tokens)
        for line in lines:
            cola = line.accept(interpreter)
            printer = SyllableTreePrinter()
            words = [syll.accept(printer) for word in line.words for syll in word.syllables]

            symbols = [y for x in cola for y in simplify_metrical_symbols(x)]
            df = pandas.DataFrame([symbols, words])
            print(df)
            print()
