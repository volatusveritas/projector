from projector import constants
from projector import expressions
from projector import types


class Token:
    def __init__(self):
        self._signature_token_type = "Null"

    def __repr__(self):
        return f"<Token: {self._signature_token_type}>"

    def getexpr(self):
        return expressions.Expression()


class SingleSymbol(Token):
    def __init__(self):
        self._signature_token_type = "SingleSymbol"
        self._signature_symbol_type = "None"

    def __repr__(self):
        return f"{super().__repr__()} [{self._signature_symbol_type}]"


class Comma(SingleSymbol):
    def __init__(self):
        super().__init__()

        self._signature_symbol_type = "Comma"


class Colon(SingleSymbol):
    def __init__(self):
        super().__init__()

        self._signature_symbol_type = "Colon"


class SymbolCouple(Token):
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


class Parentheses(SymbolCouple):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Parentheses"


class Brackets(SymbolCouple):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Brackets"


class Braces(SymbolCouple):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Braces"


class Chevrons(SymbolCouple):
    def __init__(self, closing=False):
        super().__init__(closing)

        self._signature_couple_type = "Chevrons"


class Value(Token):
    def __init__(self, refval):
        self._signature_token_type = "Value"
        self._signature_value_type = "None"

        self.refval = refval

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f" ({self._signature_value_type})"
            f" {self.refval}"
        )

    def getexpr(self):
        return expressions.ValueExpression(types.Value())


class Abacus(Value):
    def __init__(self, refval):
        super().__init__(refval)

        self._signature_value_type = "Abacus"

    def getexpr(self):
        return expressions.AbacusExpression(types.Abacus(self.refval))


class Rational(Value):
    def __init__(self, refval):
        super().__init__(refval)

        self._signature_value_type = "Rational"

    def getexpr(self):
        return expressions.RationalExpression(types.Rational(self.refval))


class Scroll(Value):
    def __init__(self, refval):
        super().__init__(refval)

        self._signature_value_type = "Scroll"

    def getexpr(self):
        return expressions.ScrollExpression(types.Scroll(self.refval))


class Lever(Value):
    def __init__(self, refval):
        super().__init__(refval)

        self._signature_value_type = "Lever"

    def getexpr(self):
        return expressions.LeverExpression(types.Lever(self.refval))


class Operator(Token):
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


class Addition(Operator):
    def __init__(self):
        super().__init__(constants.ADDITION_PRECEDENCE)

        self._signature_operator_type = "Addition"

    def getexpr(self, left=None, right=None):
        return expressions.AdditionExpression(left, right)


class Subtraction(Operator):
    def __init__(self):
        super().__init__(constants.SUBTRACTION_PRECEDENCE)

        self._signature_operator_type = "Subtraction"

    def getexpr(self, left=None, right=None):
        return expressions.SubtractionExpression(left, right)


class Multiplication(Operator):
    def __init__(self):
        super().__init__(constants.MULTIPLICATION_PRECEDENCE)

        self._signature_operator_type = "Multiplication"

    def getexpr(self, left=None, right=None):
        return expressions.MultiplicationExpression(left, right)


class Division(Operator):
    def __init__(self):
        super().__init__(constants.DIVISION_PRECEDENCE)

        self._signature_operator_type = "Division"

    def getexpr(self, left=None, right=None):
        return expressions.DivisionExpression(left, right)


class Modulo(Operator):
    def __init__(self):
        super().__init__(constants.MODULO_PRECEDENCE)

        self._signature_operator_type = "Modulo"

    def getexpr(self, left=None, right=None):
        return expressions.ModuloExpression(left, right)


class Assignment(Operator):
    def __init__(self):
        super().__init__(constants.ASSIGNMENT_PRECEDENCE)

        self._signature_operator_type = "Assignment"

    def getexpr(self, left=None, right=None):
        return expressions.AssignmentExpression(left, right)


class Identifier(Token):
    def __init__(self, name):
        self._signature_token_type = "Identifier"

        self.name = name

    def __repr__(self):
        return f"{super().__repr__()} {self.name}"

    def getexpr(self):
        return expressions.IdentifierExpression(self)


class Flow(Token):
    def __init__(self):
        self._signature_token_type = "Flow"
        self._signature_flow_type = "None"

    def __repr__(self):
        return f"{super().__repr__()} [{self._signature_flow_type}]"

    def getexpr(self):
        return expressions.FlowExpression()


class Break(Flow):
    def __init__(self):
        super().__init__()

        self._signature_flow_type = "Break"

    def getexpr(self):
        return expressions.BreakExpression()
