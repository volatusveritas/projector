import sys

from projector import types
from projector import constants
from projector import exceptions




_variable_bank = {}




class Expression:
    def __init__(self):
        self._signature_expression_type = "Null"

    def __repr__(self):
        return f"<Expression: {self._signature_expression_type}>"

    def evaluate(self):
        return None


class ValueExpression(Expression):
    def __init__(self, value):
        self._signature_expression_type = "Value"
        self._signature_value_type = "None"

        self.value = value

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f" ({self._signature_value_type})"
            f" {self.value}"
        )

    def evaluate(self):
        return self.value


class AbacusExpression(ValueExpression):
    def __init__(self, abacus_value):
        super().__init__(abacus_value)

        self._signature_value_type = "Abacus"


class RationalExpression(ValueExpression):
    def __init__(self, rational_value):
        super().__init__(rational_value)

        self._signature_value_type = "Rational"


class ScrollExpression(ValueExpression):
    def __init__(self, scroll_value):
        super().__init__(scroll_value)

        self._signature_value_type = "Scroll"


class LeverExpression(ValueExpression):
    def __init__(self, lever_value):
        super.__init__(lever_value)

        self._signature_value_type = "Lever"


class OperationExpression(Expression):
    def __init__(self, left=None, right=None):
        self._signature_expression_type = "Operation"
        self._signature_operation_type = "None"

        self.left = left
        self.right = right
        self.return_types = constants.NUMERICAL_TYPES

    def __repr__(self):
        return f"{super().__repr__()} [{self._signature_operation_type}]"

    def validate_arguments(self, left, right):
        if not isinstance(left, constants.NUMERICAL_TYPES):
            raise exceptions.TypeError(type(left))

        if not isinstance(right, constants.NUMERICAL_TYPES):
            raise exceptions.TypeError(type(right))

    def evaluate(self):
        return self.left


class AdditionExpression(OperationExpression):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)

        self._signature_operation_type = "Addition"

    def evaluate(self):
        left_term = self.left.evaluate()
        right_term = self.right.evaluate()

        if left_term is None:
            left_term = types.AbacusValue(0)

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
            raise exceptions.DivisionByZeroError

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
            raise exceptions.TypeError(type(left))

        if not isinstance(right, constants.VALUE_TYPES):
            raise exceptions.TypeError(type(right))

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

    def __repr__(self):
        return f"{super().__repr__()} '{self.name}'"

    def evaluate(self):
        if not self.name in _variable_bank:
            raise exceptions.UndefinedNameError(self.name)

        return _variable_bank[self.name]


class FlowExpression(Expression):
    def __init__(self):
        self._signature_expression_type = "Token"
        self._signature_flow_type = "None"

    def __repr__(self):
        return f"{super().__repr__()} [{self._signature_flow_type}]"


class BreakExpression(FlowExpression):
    def __init__(self):
        super().__init__()

        self._signature_flow_type = "Break"

    def evaluate(self):
        sys.exit()
