class Value:
    def __init__(self):
        self._signature_value_type = "Null"

    def __str__(self):
        return f"<Value: {self._signature_value_type}>"


class AbacusValue(Value):
    DEFAULT_VALUE = 0

    def __init__(self, initial_value=DEFAULT_VALUE):
        self._signature_value_type = "Abacus"

        self.raw_value = initial_value


class RationalValue(Value):
    DEFAULT_VALUE = 0.0

    def __init__(self, initial_value=DEFAULT_VALUE):
        self._signature_value_type = "Rational"

        self.raw_value = initial_value


class LeverValue(Value):
    DEFAULT_VALUE = False

    def __init__(self, initial_value=DEFAULT_VALUE):
        self._signature_value_type = "Lever"

        self.raw_value = initial_value


class ScrollValue(Value):
    DEFAULT_VALUE = ""

    def __init__(self, initial_value=DEFAULT_VALUE):
        self._signature_value_type = "Scroll"

        self.raw_value = initial_value
