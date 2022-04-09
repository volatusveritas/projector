from enum import Enum, auto

from projector import constants


class Type(Enum):
    DELIMITER = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()
    LITERAL = auto()
    OPERATOR = auto()


class Token:
    def __init__(self, type: Type, value: str):
        self.type: Type = type
        self.value: str = value


def tokenize(input: str) -> list[Token]:
    token_list: list[Token] = []

    index: int = -1
    while index < len(input) - 1:
        index += 1

        if input[index] in constants.WHITESPACE_CHARACTERS:
            continue

        if input[index] in constants.DECIMAL_CHARACTERS:
            number = extract_number(input, index)
            token_list.append(Token(Type.LITERAL, number))
            index += len(number) - 1
        else:
            pass

    return token_list


def tokenize_ntoken(input: str, idx: int) -> Token:
    match input[idx]:
        case "+":
            if idx < len(input) - 1 and input[idx + 1] == "=":
                return Token(Type.OPERATOR, "+=")
            else:
                return Token(Type.OPERATOR, "+")
        case "-":
            if idx < len(input) - 1 and input[idx + 1] == "-":
                return Token(Type.OPERATOR, "-=")
            else:
                return Token(Type.OPERATOR, "-")


def extract_number(input: str, start_idx: int) -> str:
    if start_idx == len(input) - 1:
        return input[start_idx]

    end_idx: int = start_idx

    for character in input[start_idx :]:
        end_idx += 1

        if character not in constants.DECIMAL_CHARACTERS:
            break

    return input[start_idx : end_idx]
