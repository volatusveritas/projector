from projector import constants
from projector import expressions


class Token:
    def __init__(self):
        self._signature_token_type = "Null"

    def __repr__(self):
        return f"<Token: {self._signature_token_type}>"

    def getexpr(self):
        return expressions.Expression()


class SingleSymbolToken(Token):
    def __init__(self):
        self._signature_token_type = "SingleSymbol"
        self._signature_symbol_type = "None"

    def __repr__(self):
        return f"{super().__repr__()} [{self._signature_symbol_type}]"


class CommaToken(SingleSymbolToken):
    def __init__(self):
        super().__init__()

        self._signature_symbol_type = "Comma"


class SymbolCoupleToken(Token):
    def __init__(self, closing=False):
        self._signature_token_type = "SymbolCouple"
        self._signature_couple_type = "None"
        self._signature_delim_type = "Close" if closing else "Open"

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f" [{self._signature_couple_type}]"
            f" {self._signature_delim_type}"
        )


class ParenthesesToken(SymbolCoupleToken):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Parentheses"


class BracketsToken(SymbolCoupleToken):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Brackets"


class BracesToken(SymbolCoupleToken):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Braces"


class ChevronsToken(SymbolCoupleToken):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Chevrons"


class ValueToken(Token):
    def __init__(self, value):
        self._signature_token_type = "Value"
        self._signature_value_type = "None"

        self.value = value

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f" ({self._signature_value_type})"
            f" {self.value}"
        )

    def getexpr(self):
        return expressions.ValueExpression(self.value)


class IntegerToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "Integer"

    def getexpr(self):
        return expressions.AbacusExpression(self.value)


class FloatToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "Float"

    def getexpr(self):
        return expressions.RationalExpression(self.value)


class StringToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "String"

    def getexpr(self):
        return expressions.ScrollExpression(self.value)


class BoolToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "Bool"

    def getexpr(self):
        return expressions.LeverExpression(self.value)


class OperatorToken(Token):
    def __init__(self, precedence=0):
        self._signature_token_type = "Operator"
        self._signature_operator_type = "None"

        self.precedence = precedence

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f" [{self._signature_operator_type}]"
            f" P:{self.precedence}"
        )

    def getexpr(self, left=None, right=None):
        return expressions.OperationExpression(left, right)


class AdditionToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.ADDITION_PRECEDENCE)

        self._signature_operator_type = "Addition"

    def getexpr(self, left=None, right=None):
        return expressions.AdditionExpression(left, right)


class SubtractionToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.SUBTRACTION_PRECEDENCE)

        self._signature_operator_type = "Subtraction"

    def getexpr(self, left=None, right=None):
        return expressions.SubtractionExpression(left, right)


class MultiplicationToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.MULTIPLICATION_PRECEDENCE)

        self._signature_operator_type = "Multiplication"

    def getexpr(self, left=None, right=None):
        return expressions.MultiplicationExpression(left, right)


class DivisionToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.DIVISION_PRECEDENCE)

        self._signature_operator_type = "Division"

    def getexpr(self, left=None, right=None):
        return expressions.DivisionExpression(left, right)


class ModuloToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.MODULO_PRECEDENCE)

        self._signature_operator_type = "Modulo"

    def getexpr(self, left=None, right=None):
        return expressions.ModuloExpression(left, right)


class AssignmentToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.ASSIGNMENT_PRECEDENCE)

        self._signature_operator_type = "Assignment"

    def getexpr(self, left=None, right=None):
        return expressions.AssignmentExpression(left, right)


class IdentifierToken(Token):
    def __init__(self, name):
        self._signature_token_type = "Identifier"

        self.name = name

    def __repr__(self):
        return f"{super().__repr__()} {self.name}"

    def getexpr(self):
        return expressions.IdentifierExpression(self)


class FlowToken(Token):
    def __init__(self):
        self._signature_token_type = "Flow"
        self._signature_flow_type = "None"

    def __repr__(self):
        return f"{super().__repr__()} [{self._signature_flow_type}]"

    def getexpr(self):
        return expressions.FlowExpression()


class BreakToken(FlowToken):
    def __init__(self):
        super().__init__()

        self._signature_flow_type = "Break"

    def getexpr(self):
        return expressions.BreakExpression()
