class Expression:
    def __init__(self):
        self._signature_expression_type = "Null"

    def __str__(self):
        return f"<Token: Expression> ({self._signature_expression_type})"

    def evaluate(self):
        return None


class ValueExpression(Expression):
    def __init__(self, value_token):
        self._signature_expression_type = "Value"
        self._signature_value_type = "None"

        self.value = value_token.value

    def __str__(self):
        return f"{str(super())} ({self._signature_value_type}) {self.value}"

    def evaluate(self):
        return self.value


class OperationExpression(Expression):
    def __init__(self, left=None, right=None):
        self._signature_expression_type = "Operation"
        self._signature_operation_type = "None"

        self.left = left
        self.right = right

    def __str__(self):
        return f"{str(super())} [{self._signature_operation_type}]"


class AdditionOperationExpression(OperationExpression):
    def __init__(self):
        super().__init__()

        self._signature_operation_type = "Addition"

    def evaluate(self):
        left_term = self.left.evaluate()
        right_term = self.right.evaluate()

        if left_term is None:
            left_term = 0

        return left_term + right_term


class SubtractionOperationExpression(OperationExpression):
    def __init__(self):
        super().__init__()

        self._signature_operation_type = "Subtraction"

    def evaluate(self):
        left_term = self.left.evaluate()
        right_term = self.right.evaluate()

        if left_term is None:
            left_term = 0

        return left_term - right_term


class MultiplicationOperationExpression(OperationExpression):
    def __init__(self):
        super().__init__()

        self._signature_operation_type = "Multiplication"

    def evaluate(self):
        left_factor = self.left.evaluate()
        right_factor = self.right.evaluate()

        return left_factor * right_factor


class DivisionOperationExpression(OperationExpression):
    def __init__(self):
        super().__init__()

        self._signature_operation_type = "Division"

    def evaluate(self):
        dividend = self.left.evaluate()
        divisor = self.right.evaluate()

        return dividend // divisor


class ModuloOperationExpression(OperationExpression):
    def __init__(self):
        super().__init__()

        self._signature_operation_type = "Modulo"

    def evaluate(self):
        dividend = self.left.evaluate()
        divisor = self.right.evaluate()

        return dividend % divisor


class AssignmentOperationExpression(OperationExpression):
    def __init__(self):
        super().__init__()

        self._signature_operation_type = "Assignment"

    def evaluate(self, variable_bank):
        value = self.right.evaluate()

        variable_bank[self.left.name] = value

        return None


class IdentifierExpression(Expression):
    def __init__(self, identifier_token):
        super().__init__()

        self._signature_expression_type = "Identifier"

        self.name = identifier_token.name

    def __str__(self):
        return f"{str(super())} '{self.name}'"

    def evaluate(self, variable_bank):
        return variable_bank[self.name]
