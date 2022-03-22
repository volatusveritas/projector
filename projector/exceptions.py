from projector import constants


class ProjectorError(Exception):
    def __str__(self):
        return "Unknown error"


class ProjectorTypeError(ProjectorError):
    def __str__(self, type=constants.ABSENT_SYMBOL_NAME):
        return f"Invalid type '{type}'"


class ProjectorValueError(ProjectorError):
    def __str__(self, value=constants.ABSENT_SYMBOL_NAME):
        return f"Invalid value '{value}'"


class ProjectorDivisionByZeroError(ProjectorError):
    def __str__(self):
        return "Division by zero"


class ProjectorUndefinedNameError(ProjectorError):
    def __str__(self, name=constants.ABSENT_SYMBOL_NAME):
        return f"Undefined name '{name}'"


class ProjectorOperatorAbsentError(ProjectorError):
    def __str__(self):
        return "Operator absent"


class ProjectorUnmatchedParenthesesError(ProjectorError):
    def __str__(self):
        return "Unmatched parentheses"


class ProjectorInvalidSymbolError(ProjectorError):
    def __str__(self, symbol=constants.ABSENT_SYMBOL_NAME):
        return f"Invalid symbol '{symbol}'"


class ProjectorMissingInitArgError(ProjectorError):
    def __str__(self, argument=constants.ABSENT_SYMBOL_NAME):
        return f"Missing initialization argument '{argument}'"


class ProjectorCantOpenFileError(ProjectorError):
    def __str__(self, file=constants.ABSENT_SYMBOL_NAME):
        return f"Unable to open file '{file}'"
