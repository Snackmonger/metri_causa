from src.metri_causa import LengthTest


def test_nonnus() -> None:
    with open("tests/texts/nonnus.txt", encoding="utf8") as f:
        text = f.read()
        LengthTest(text)

def test_homer() -> None:
    with open("tests/texts/homer.txt", encoding="utf8") as f:
        text = f.read()
        LengthTest(text)


def test_anomalies() -> None:
    with open("tests/texts/anomalies.txt", encoding="utf8") as f:
        text = f.read()
        LengthTest(text)

