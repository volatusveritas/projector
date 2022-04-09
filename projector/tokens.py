from projector.constants import *


class Token:
    _signature_token_type: str = "Null"

    def __repr__(self) -> str:
        return f"<Token: {self._signature_token_type}>"


class SingleSymbol(Token):
    _signature_token_type = "SingleSymbol"
    _signature_symbol_type: str = "None"

    def __repr__(self) -> str:
        return f"{super().__repr__()} [{self._signature_symbol_type}]"


class Comma(SingleSymbol):
    _signature_symbol_type = "Comma"


class Colon(SingleSymbol):
    _signature_symbol_type = "Colon"


class SymbolCouple(Token):
    _signature_token_type = "SymbolCouple"
    _signature_couple_type: str = "None"

    def __init__(self, closing:bool=False) -> None:
        self._signature_delim_type: str = "Close" if closing else "Open"

    def __repr__(self) -> str:
        return (
            f"{super().__repr__()}"
            f" [{self._signature_couple_type}]"
            f" {self._signature_delim_type}"
        )


class Parentheses(SymbolCouple):
    _signature_couple_type = "Parentheses"

    def __init__(self, closing:bool=False):
        super().__init__(closing)


class Brackets(SymbolCouple):
    _signature_couple_type = "Brackets"

    def __init__(self, closing:bool=False) -> None:
        super().__init__(closing)


class Braces(SymbolCouple):
    _signature_couple_type = "Braces"

    def __init__(self, closing:bool=False) -> None:
        super().__init__(closing)


class Chevrons(SymbolCouple):
    _signature_couple_type = "Chevrons"

    def __init__(self, closing:bool=False):
        super().__init__(closing)


class Value(Token):
    _signature_token_type = "Value"
    _signature_value_type: str = "None"

    def __init__(self, refval:str) -> None:
        self.refval: str = refval

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f" ({self._signature_value_type})"
            f" {self.refval}"
        )


class Integer(Value):
    _signature_value_type = "Integer"

    def __init__(self, refval:str) -> None:
        super().__init__(refval)


class Rational(Value):
    _signature_value_type = "Float"

    def __init__(self, refval:str) -> None:
        super().__init__(refval)


class Text(Value):
    _signature_value_type = "Text"

    def __init__(self, refval:str) -> None:
        super().__init__(refval)


class Boolean(Value):
    _signature_value_type: str = "Boolean"

    def __init__(self, refval:str) -> None:
        super().__init__(refval)


class Operator(Token):
    _signature_token_type = "Operator"
    _signature_operator_type: str = "None"

    def __init__(self, precedence:int=0):
        self.precedence:int = precedence

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f" [{self._signature_operator_type}]"
            f" P:{self.precedence}"
        )


class Plus(Operator):
    _signature_operator_type = "Plus"

    def __init__(self):
        super().__init__(ADDITION_PRECEDENCE)


class Minus(Operator):
    _signature_operator_type = "Minus"

    def __init__(self):
        super().__init__(SUBTRACTION_PRECEDENCE)


class Asterisk(Operator):
    _signature_operator_type = "Asterisk"

    def __init__(self):
        super().__init__(MULTIPLICATION_PRECEDENCE)


class Division(Operator):
    _signature_operator_type = "Division"

    def __init__(self):
        super().__init__(DIVISION_PRECEDENCE)


class Modulo(Operator):
    _signature_operator_type = "Modulo"

    def __init__(self):
        super().__init__(MODULO_PRECEDENCE)


class Assignment(Operator):
    _signature_operator_type = "Assignment"

    def __init__(self):
        super().__init__(ASSIGNMENT_PRECEDENCE)


class Identifier(Token):
    _signature_token_type = "Identifier"

    def __init__(self, name: str):
        self.name: str = name

    def __repr__(self):
        return f"{super().__repr__()} {self.name}"


class Flow(Token):
    _signature_token_type = "Flow"
    _signature_flow_type: str = "None"

    def __repr__(self):
        return f"{super().__repr__()} [{self._signature_flow_type}]"


class Break(Flow):
    _signature_flow_type = "Break"
