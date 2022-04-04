from projector import constants


class Error(Exception):
    def __str__(self):
        return "Unknown error"


class TypeError(Error):
    def __init__(self, typename=constants.ABSENT_SYMBOL_NAME):
        self.typename = typename

    def __str__(self):
        return f"Invalid type '{self.typename}'"


class ValueError(Error):
    def __init__(self, value=constants.ABSENT_SYMBOL_NAME):
        self.value = value

    def __str__(self):
        return f"Invalid value '{self.value}'"


class DivisionByZeroError(Error):
    def __str__(self):
        return "Division by zero"


class UndefinedNameError(Error):
    def __init__(self, name=constants.ABSENT_SYMBOL_NAME):
        self.name = name

    def __str__(self):
        return f"Undefined name '{self.name}'"


class OperatorAbsentError(Error):
    def __str__(self):
        return "Operator absent"


class UnmatchedParenthesesError(Error):
    def __str__(self):
        return "Unmatched parentheses"


class UnmatchedQuotesError(Error):
    def __str__(self):
        return "Unmatched quotes"


class InvalidSymbolError(Error):
    def __init__(self, symbol=constants.ABSENT_SYMBOL_NAME):
        self.symbol = symbol

    def __str__(self):
        return f"Invalid symbol '{self.symbol}'"


class MissingInitArgError(Error):
    def __init__(self, argument=constants.ABSENT_SYMBOL_NAME):
        self.argument = argument

    def __str__(self):
        return f"Missing initialization argument '{self.argument}'"


class CantOpenFileError(Error):
    def __init__(self, file=constants.ABSENT_SYMBOL_NAME):
        self.file = file

    def __str__(self):
        return f"Unable to open file '{self.file}'"
