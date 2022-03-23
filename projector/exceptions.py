from projector import constants


class ProjectorError(Exception):
    def __str__(self):
        return "Unknown error"


class ProjectorTypeError(ProjectorError):
    def __init__(self, type=constants.ABSENT_SYMBOL_NAME):
        self.type = type

    def __str__(self):
        return f"Invalid type '{self.type}'"


class ProjectorValueError(ProjectorError):
    def __init__(self, value=constants.ABSENT_SYMBOL_NAME):
        self.value = value

    def __str__(self):
        return f"Invalid value '{self.value}'"


class ProjectorDivisionByZeroError(ProjectorError):
    def __str__(self):
        return "Division by zero"


class ProjectorUndefinedNameError(ProjectorError):
    def __init__(self, name=constants.ABSENT_SYMBOL_NAME):
        self.name = name

    def __str__(self):
        return f"Undefined name '{self.name}'"


class ProjectorOperatorAbsentError(ProjectorError):
    def __str__(self):
        return "Operator absent"


class ProjectorUnmatchedParenthesesError(ProjectorError):
    def __str__(self):
        return "Unmatched parentheses"


class ProjectorInvalidSymbolError(ProjectorError):
    def __init__(self, symbol=constants.ABSENT_SYMBOL_NAME):
        self.symbol = symbol

    def __str__(self):
        return f"Invalid symbol '{self.symbol}'"


class ProjectorMissingInitArgError(ProjectorError):
    def __init__(self, argument=constants.ABSENT_SYMBOL_NAME):
        self.argument = argument

    def __str__(self):
        return f"Missing initialization argument '{self.argument}'"


class ProjectorCantOpenFileError(ProjectorError):
    def __init__(self, file=constants.ABSENT_SYMBOL_NAME):
        self.file = file

    def __str__(self):
        return f"Unable to open file '{self.file}'"
