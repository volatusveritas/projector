import projector.exceptions as exceptions




_variable_bank = {}




class Expression:
    def __init__(self):
        self._signature_expression_type = "Null"

    def __str__(self):
        return f"<Expression: {self._signature_expression_type}>"

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


class IntegerValueExpression(ValueExpression):
    def __init__(self, integer_token):
        super().__init__(integer_token)

        self._signature_value_type = "Integer"


class FloatValueExpression(ValueExpression):
    def __init__(self, float_token):
        super().__init__(float_token)

        self._signature_value_type = "Float"


class StringValueExpression(ValueExpression):
    def __init__(self, string_token):
        super().__init__(string_token)

        self._signature_value_type = "String"


class BoolValueExpression(ValueExpression):
    def __init__(self, bool_token):
        super.__init__(bool_token)

        self._signature_value_type = "Bool"


class OperationExpression(Expression):
    def __init__(self, left=None, right=None):
        self._signature_expression_type = "Operation"
        self._signature_operation_type = "None"

        self.left = left
        self.right = right

    def __str__(self):
        return f"{str(super())} [{self._signature_operation_type}]"

    def evaluate(self):
        return (self.left, self.right)


class AdditionOperationExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Addition"

    def evaluate(self):
        left_term = self.left.evaluate()
        right_term = self.right.evaluate()

        if left_term is None:
            left_term = 0

        if not isinstance(left_term, (int, float)):
            raise exceptions.ProjectorTypeError(type(left_term))

        if not isinstance(right_term, (int, float)):
            raise exceptions.ProjectorTypeError(type(right_term))

        return left_term + right_term


class SubtractionOperationExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Subtraction"

    def evaluate(self):
        left_term = self.left.evaluate()
        right_term = self.right.evaluate()

        if left_term is None:
            left_term = 0

        if not isinstance(left_term, (int, float)):
            raise exceptions.ProjectorTypeError(type(left_term))

        if not isinstance(right_term, (int, float)):
            raise exceptions.ProjectorTypeError(type(right_term))

        return left_term - right_term


class MultiplicationOperationExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Multiplication"

    def evaluate(self):
        left_factor = self.left.evaluate()
        right_factor = self.right.evaluate()

        if not isinstance(left_factor, (int, float)):
            raise exceptions.ProjectorTypeError(type(left_factor))

        if not isinstance(right_factor, (int, float)):
            raise exceptions.ProjectorTypeError(type(right_factor))

        return left_factor * right_factor


class DivisionOperationExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Division"

    def evaluate(self):
        dividend = self.left.evaluate()
        divisor = self.right.evaluate()

        if not isinstance(dividend, (int, float)):
            raise exceptions.ProjectorTypeError(type(dividend))

        if not isinstance(divisor, (int, float)):
            raise exceptions.ProjectorTypeError(type(divisor))

        elif not divisor:
            raise exceptions.ProjectorDivisionByZeroError

        return dividend // divisor


class ModuloOperationExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Modulo"

    def evaluate(self):
        dividend = self.left.evaluate()
        divisor = self.right.evaluate()

        if not isinstance(dividend, (int, float)):
            raise exceptions.ProjectorTypeError(type(dividend))

        if not isinstance(divisor, (int, float)):
            raise exceptions.ProjectorTypeError(type(divisor))

        elif not divisor:
            raise exceptions.ProjectorDivisionByZeroError

        return dividend % divisor


class AssignmentOperationExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Assignment"

    def evaluate(self):
        value = self.right.evaluate()

        if not isinstance(self.left, IdentifierExpression):
            raise exceptions.ProjectorTypeError(type(self.left))

        _variable_bank[self.left.name] = value

        return None


class IdentifierExpression(Expression):
    def __init__(self, identifier_token):
        super().__init__()

        self._signature_expression_type = "Identifier"

        self.name = identifier_token.name

    def __str__(self):
        return f"{str(super())} '{self.name}'"

    def evaluate(self):
        if not self.name in _variable_bank:
            raise exceptions.ProjectorUndefinedNameError(self.name)

        return _variable_bank[self.name]
