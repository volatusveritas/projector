class ProjectorError(Exception):
    def __init__(self, code="000", message="An unknown error occurred"):
        self.code = code
        self.message = message

    def __str__(self):
        return f"PJ{self.code}: {self.message}"


class ProjectorTypeError(ProjectorError):
    def __init__(self, context, type_name, extra=""):
        super().__init__(
            "001", f"Invalid value type '{type_name}' at {context}{extra}"
        )


class ProjectorValueError(ProjectorError):
    def __init__(self, context):
        super().__init__("002", f"Invalid value at {context}")


class ProjectorDivisionByZeroError(ProjectorError):
    def __init__(self, context):
        super().__init__("003", f"Division by zero at {context}")


class ProjectorUndefinedNameError(ProjectorError):
    def __init__(self, context, name, extra=""):
        super().__init__("004", f"Undefined name '{name}' at {context}{extra}")
