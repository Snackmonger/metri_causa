from src import constants, utils


def test_get_char_attrs() -> None:
    for char in constants.ALPHA_VARIANTS:
        print(utils.get_char_attrs(char))