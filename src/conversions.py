

from enum import StrEnum, auto


class Homer(StrEnum):
    ILIAD = auto()
    ODYSSEY = auto()


class HomerLetter:
    def __init__(self) -> None:
        self.__conversion: dict[str, int] = {'A': 1,
                                             'B': 2,
                                             'G': 3,
                                             'D': 4,
                                             'E': 5,
                                             'Z': 6,
                                             'H': 7,
                                             'Q': 8,
                                             'I': 9,
                                             'K': 10,
                                             'L': 11,
                                             'M': 12,
                                             'N': 13,
                                             'C': 14,
                                             'O': 15,
                                             'P': 16,
                                             'R': 17,
                                             'S': 18,
                                             'T': 19,
                                             'U': 20,
                                             'F': 21,
                                             'X': 22,
                                             'Y': 23,
                                             'W': 24}

    def iliad(self, number: int, beta: bool = False) -> str:
        ...

    def odyssey(self, number: int, beta: bool = False) -> str:
        ...

    def identify(self, letter: str) -> int:
        ...
