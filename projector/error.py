class ProjectorError(Exception):
    def __init__(self,
        code="000", message="An unknown error occurred",
        context="unknown execution point"
    ):
        self.code = code
        self.message = message
        self.context = context

    def __str__(self):
        return f"PJ{self.code}: {self.message} at {self.context}"


class ProjectorTypeError(ProjectorError):
    def __init__(self, context, type, extra=""):
        super().__init__(
            "001", f"Invalid value type '{type}'", f"{context}{extra}"
        )


class ProjectorValueError(ProjectorError):
    def __init__(self, context, extra=""):
        super().__init__("002", "Invalid value", f"{context}{extra}")


class ProjectorDivisionByZeroError(ProjectorError):
    def __init__(self, context, extra=""):
        super().__init__("003", "Division by zero", f"{context}{extra}")


class ProjectorUndefinedNameError(ProjectorError):
    def __init__(self, context, name, extra=""):
        super().__init__(
            "004", f"Undefined name '{name}'", f"{context}{extra}"
        )


class ProjectorOperatorAbsentError(ProjectorError):
    def __init__(self, extra=""):
        super().__init__("010", "Expected operator", f"parsing{extra}")


class ProjectorUnmatchedParenthesesError(ProjectorError):
    def __init__(self, extra=""):
        super().__init__("020", "Unmatched parentheses", f"tokenization{extra}")


class ProjectorInvalidSymbolError(ProjectorError):
    def __init__(self, symbol, extra=""):
        super().__init__(
            "021", f"Invalid symbol '{symbol}'", f"tokenization{extra}"
        )
