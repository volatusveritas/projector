from projector import constants
from projector import expressions




class Token:
    def __init__(self):
        self._signature_token_type = "Null"

    def __str__(self):
        return f"<Token: {self._signature_token_type}>"

    def getexpr(self):
        return expressions.Expression()


class ValueToken(Token):
    def __init__(self, value):
        self._signature_token_type = "Value"
        self._signature_value_type = "None"

        self.value = value

    def __str__(self):
        return f"{str(super())} ({self._signature_value_type}) {self.value}"

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
            f"{str(super())} "
            f"[{self._signature_operator_type}] "
            f"P:{self.precedence}"
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
        return f"{str(super())} {self.name}"

    def getexpr(self):
        return expressions.IdentifierExpression(self)


class FlowToken(Token):
    def __init__(self):
        self._signature_token_type = "Flow"
        self._signature_flow_type = "None"

    def __str__(self):
        return f"{str(super())} [{self._signature_flow_type}]"

    def getexpr(self):
        return expressions.FlowExpression()


class BreakFlowToken(FlowToken):
    def __init__(self):
        super().__init__()

        self._signature_flow_type = "Break"

    def getexpr(self):
        return expressions.BreakFlowExpression()


class TokenGroup(Token):
    def __init__(self, token_list=[]):
        self._token_list = token_list
        self.operative, self.nested = self.get_attributes()

    def __len__(self):
        return len(self._token_list)

    def __getitem__(self, key):
        return self._token_list[key]

    def __iter__(self):
        return iter(self._token_list)

    def __bool__(self):
        return bool(self._token_list)

    def __str__(self, indent_level=0):
        hash_signature = hash(self)
        indent_padding = indent_level * '\t'

        group_string = f"{indent_padding}<Token: GRP -- {hash_signature}"

        if self.operative:
            group_string += " (operative)"

        if self.nested:
            group_string += " (nested)"

        for token in self._token_list:
            if isinstance(token, TokenGroup):
                group_string += f"\n{token.__str__(indent_level + 1)}"
            else:
                group_string += f"\n{indent_padding}\t{str(token)}"

        group_string += f"\n{indent_padding}{hash_signature} -- >"

        return group_string

    def get_attributes(self):
        operative = False
        nested = False

        for token in self._token_list:
            if isinstance(token, OperatorToken):
                operative = True
            elif isinstance(token, TokenGroup):
                nested = True

            if operative and nested:
                break

        return operative, nested
