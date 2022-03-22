class ProjectorError(Exception):
    def __str__(self):
        return "Unknown error"


class ProjectorTypeError(ProjectorError):
    def __str__(self):
        return "Invalid type"


class ProjectorValueError(ProjectorError):
    def __str__(self):
        return "Invalid value"


class ProjectorDivisionByZeroError(ProjectorError):
    def __str__(self):
        return "Division by zero"


class ProjectorUndefinedNameError(ProjectorError):
    def __str__(self):
        return "Undefined name"


class ProjectorOperatorAbsentError(ProjectorError):
    def __str__(self):
        return "Operator absent"


class ProjectorUnmatchedParenthesesError(ProjectorError):
    def __str__(self):
        return "Unmatched parentheses"


class ProjectorInvalidSymbolError(ProjectorError):
    def __str__(self):
        return "Invalid symbol"
