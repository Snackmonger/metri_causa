from src.metri_causa import LengthTest


def test_nonnus() -> None:
    with open("tests/texts/nonnus.txt", encoding="utf8") as f:
        text = f.read()
        __test_scansion(text)


def __test_scansion(text: str) -> None:
    LengthTest(text)