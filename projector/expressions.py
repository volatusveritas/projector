import sys

import projector.constants as constants
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


class IntegerExpression(ValueExpression):
    def __init__(self, integer_token):
        super().__init__(integer_token)

        self._signature_value_type = "Integer"


class FloatExpression(ValueExpression):
    def __init__(self, float_token):
        super().__init__(float_token)

        self._signature_value_type = "Float"


class StringExpression(ValueExpression):
    def __init__(self, string_token):
        super().__init__(string_token)

        self._signature_value_type = "String"


class BoolExpression(ValueExpression):
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

    def validate_arguments(self, left, right):
        if not isinstance(left, constants.NUMERICAL_TYPES):
            raise exceptions.ProjectorTypeError(type(left))

        if not isinstance(right, constants.NUMERICAL_TYPES):
            raise exceptions.ProjectorTypeError(type(right))

    def evaluate(self):
        return (self.left, self.right)


class AdditionExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Addition"

    def evaluate(self):
        left_term = self.left.evaluate()
        right_term = self.right.evaluate()

        if left_term is None:
            left_term = 0

        self.validate_arguments(left_term, right_term)

        return left_term + right_term


class SubtractionExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Subtraction"

    def evaluate(self):
        left_term = self.left.evaluate()
        right_term = self.right.evaluate()

        if left_term is None:
            left_term = 0

        self.validate_arguments(left_term, right_term)

        return left_term - right_term


class MultiplicationExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Multiplication"

    def evaluate(self):
        left_factor = self.left.evaluate()
        right_factor = self.right.evaluate()

        self.validate_arguments(left_factor, right_factor)

        return left_factor * right_factor


class DivisionExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Division"

    def validate_arguments(self, left, right):
        super().validate_arguments(left, right)

        if not right:
            raise exceptions.ProjectorDivisionByZeroError

    def evaluate(self):
        dividend = self.left.evaluate()
        divisor = self.right.evaluate()

        self.validate_arguments(dividend, divisor)

        return dividend // divisor


class ModuloExpression(DivisionExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Modulo"

    def evaluate(self):
        dividend = self.left.evaluate()
        divisor = self.right.evaluate()

        self.validate_arguments(dividend, divisor)

        return dividend % divisor


class AssignmentExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Assignment"

    def validate_arguments(self, left, right):
        if not isinstance(left, IdentifierExpression):
            raise exceptions.ProjectorTypeError(type(left))

        if not isinstance(right, constants.VALUE_TYPES):
            raise exceptions.ProjectorTypeError(type(right))

    def evaluate(self):
        value = self.right.evaluate()

        self.validate_arguments(self.left, value)

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


class FlowExpression(Expression):
    def __init__(self):
        self._signature_expression_type = "Token"
        self._signature_flow_type = "None"

    def __str__(self):
        return f"{str(super())} [{self._signature_flow_type}]"


class BreakExpression(FlowExpression):
    def __init__(self):
        super().__init__()

        self._signature_flow_type = "Break"

    def evaluate(self):
        sys.exit()
