import projector.constants as constants




class Token:
    def __init__(self):
        self._signature_token_type = "Null"

    def __str__(self):
        return f"<Token: {self._signature_token_type}>"


class ValueToken(Token):
    def __init__(self, value):
        self._signature_token_type = "Value"
        self._signature_value_type = "None"

        self.value = value

    def __str__(self):
        return f"{str(super())} ({self._signature_value_type}) {self.value}"


class IntegerValueToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "Integer"


class FloatValueToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "Float"


class StringValueToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "String"


class BoolValueToken(ValueToken):
    def __init__(self, value):
        super().__init__(value)

        self._signature_value_type = "Bool"


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


class AdditionOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.ADDITION_PRECEDENCE)

        self._signature_operator_type = "Addition"


class SubtractionOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.SUBTRACTION_PRECEDENCE)

        self._signature_operator_type = "Subtraction"


class MultiplicationOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.MULTIPLICATION_PRECEDENCE)

        self._signature_operator_type = "Multiplication"


class DivisionOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.DIVISION_PRECEDENCE)

        self._signature_operator_type = "Division"


class ModuloOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.MODULO_PRECEDENCE)

        self._signature_operator_type = "Modulo"


class AssignmentOperatorToken(OperatorToken):
    def __init__(self):
        super().__init__(constants.ASSIGNMENT_PRECEDENCE)

        self._signature_operator_type = "Assignment"


class IdentifierToken(Token):
    def __init__(self, name):
        self._signature_token_type = "Identifier"

        self.name = name

    def __str__(self):
        return f"{str(super())} {self.name}"


class FlowToken(Token):
    def __init__(self):
        self._signature_token_type = "Flow"
        self._signature_flow_type = "None"

    def __str__(self):
        return f"{str(super())} [{self._signature_flow_type}]"


class BreakFlowToken(FlowToken):
    def __init__(self):
        super().__init__()

        self._signature_flow_type = "Break"


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
