class ProjectorError(Exception):
    def __init__(self, code="000", message="An unknown error occurred"):
        self.code = code
        self.message = message

    def __str__(self):
        return f"PJ{self.code}: {self.message}"
