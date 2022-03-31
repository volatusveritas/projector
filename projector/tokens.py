from projector import constants
from projector import expressions




class Token:
    def __init__(self):
        self._signature_token_type = "Null"

    def __str__(self):
        return f"<Token: {self._signature_token_type}>"

    def getexpr(self):
        return expressions.Expression()


class SingleSymbolToken(Token):
    def __init__(self):
        self._signature_token_type = "SingleSymbol"
        self._signature_symbol_type = "None"

    def __str__(self):
        return f"{super().__str__()} [{self._signature_symbol_type}]"


class CommaSingleSymbolToken(SingleSymbolToken):
    def __init__(self):
        self._signature_symbol_type = "Comma"


class SymbolCoupleToken(Token):
    def __init__(self, closing=False):
        self._signature_token_type = "SymbolCouple"
        self._signature_couple_type = "None"
        self._signature_delim_type = "Close" if closing else "Open"

    def __str__(self):
        return (
            f"{super().__str__()}"
            f" [{self._signature_couple_type}"
            f" {self._signature_delim_type}]"
        )


class ParenthesesSymbolCoupleToken(SymbolCoupleToken):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Parentheses"


class BracketsSymbolCoupleToken(SymbolCoupleToken):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Brackets"


class BracesSymbolCoupleToken(SymbolCoupleToken):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Braces"


class ChevronsSymbolCoupleToken(SymbolCoupleToken):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Chevrons"


class ValueToken(Token):
    def __init__(self, value):
        self._signature_token_type = "Value"
        self._signature_value_type = "None"

        self.value = value

    def __str__(self):
        return (
            f"{super().__str__()}"
            f" ({self._signature_value_type})"
            f" {self.value}"
        )

    def getexpr(self):
        return expressions.ValueExpression(self)


class IntegerValueToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "Integer"

    def getexpr(self):
        return expressions.IntegerValueExpression(self)


class FloatValueToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "Float"

    def getexpr(self):
        return expressions.FloatValueExpression(self)


class StringValueToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "String"

    def getexpr(self):
        return expressions.StringValueExpression(self)


class BoolValueToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "Bool"

    def getexpr(self):
        return expressions.BoolValueExpression(self)


class OperatorToken(Token):
    def __init__(self, precedence=0):
        self._signature_token_type = "Operator"
        self._signature_operator_type = "None"

        self.precedence = precedence

    def __str__(self):
        return (
            f"{super().__str__()}"
            f" [{self._signature_operator_type}]"
            f" P:{self.precedence}"
        )

    def getexpr(self, left=None, right=None):
        return expressions.OperationExpression(left, right)


class AdditionOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.ADDITION_PRECEDENCE)

        self._signature_operator_type = "Addition"

    def getexpr(self, left=None, right=None):
        return expressions.AdditionOperationExpression(left, right)


class SubtractionOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.SUBTRACTION_PRECEDENCE)

        self._signature_operator_type = "Subtraction"

    def getexpr(self, left=None, right=None):
        return expressions.SubtractionOperationExpression(left, right)


class MultiplicationOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.MULTIPLICATION_PRECEDENCE)

        self._signature_operator_type = "Multiplication"

    def getexpr(self, left=None, right=None):
        return expressions.MultiplicationOperationExpression(left, right)


class DivisionOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.DIVISION_PRECEDENCE)

        self._signature_operator_type = "Division"

    def getexpr(self, left=None, right=None):
        return expressions.DivisionOperationExpression(left, right)


class ModuloOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.MODULO_PRECEDENCE)

        self._signature_operator_type = "Modulo"

    def getexpr(self, left=None, right=None):
        return expressions.ModuloOperationExpression(left, right)


class AssignmentOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.ASSIGNMENT_PRECEDENCE)

        self._signature_operator_type = "Assignment"

    def getexpr(self, left=None, right=None):
        return expressions.AssignmentOperationExpression(left, right)


class IdentifierToken(Token):
    def __init__(self, name):
        self._signature_token_type = "Identifier"

        self.name = name

    def __str__(self):
        return f"{super().__str__()} {self.name}"

    def getexpr(self):
        return expressions.IdentifierExpression(self)


class FlowToken(Token):
    def __init__(self):
        self._signature_token_type = "Flow"
        self._signature_flow_type = "None"

    def __str__(self):
        return f"{super().__str__()} [{self._signature_flow_type}]"

    def getexpr(self):
        return expressions.FlowExpression()


class BreakFlowToken(FlowToken):
    def __init__(self):
        super().__init__()

        self._signature_flow_type = "Break"

    def getexpr(self):
        return expressions.BreakFlowExpression()
