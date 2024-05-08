from src.metri_causa import LengthTest2


def test_nonn() -> None:
    with open("tests/texts/nonnus.txt", encoding="utf8") as f:
        text = f.read()
        test_scansion(text)


def test_scansion(text: str) -> None:
    LengthTest2(text)