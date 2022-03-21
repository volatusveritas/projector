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
    def __init__(self, context, type_name, extra=""):
        super().__init__(
            "001", f"Invalid value type '{type_name}'", f"{context}{extra}"
        )


class ProjectorValueError(ProjectorError):
    def __init__(self, context, extra=""):
        super().__init__("002", f"Invalid value", f"{context}{extra}")


class ProjectorDivisionByZeroError(ProjectorError):
    def __init__(self, context, extra=""):
        super().__init__("003", f"Division by zero", f"{context}{extra}")


class ProjectorUndefinedNameError(ProjectorError):
    def __init__(self, context, name, extra=""):
        super().__init__(
            "004", f"Undefined name '{name}'", f"{context}{extra}"
        )
