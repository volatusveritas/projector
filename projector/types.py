from projector import exceptions




class Value:
    DEFAULT_VALUE = None

    def __init__(self, initial_value=DEFAULT_VALUE):
        self._signature_value_type = "Null"

        self.raw_value = initial_value

    def __repr__(self):
        return f"<Value: {self._signature_value_type}>"

    def __str__(self):
        return str(self.raw_value)

    def to_lever(self):
        return LeverValue(False)


class AbacusValue(Value):
    DEFAULT_VALUE = 0
    ORDER = 2

    def __init__(self, initial_value=DEFAULT_VALUE):
        super().__init__(initial_value)

        self._signature_value_type = "Abacus"

    def to_abacus(self):
        return self

    def to_rational(self):
        return RationalValue(float(self.raw_value))

    def to_lever(self):
        return LeverValue(bool(self.raw_value))

    # TODO: Stop the insane repetition in these function checks
    def add(self, other):
        if other.ORDER > self.ORDER:
            if not hasattr(other, "add"):
                raise exceptions.ProjectorTypeError(type(other))

            return other.add(self)

        if other.ORDER < self.ORDER:
            if not hasattr(other, "to_abacus"):
                raise exceptions.ProjectorTypeError(type(other))

            other = other.to_abacus()

        return AbacusValue(self.raw_value + other.raw_value)

    def subtract(self, other):
        if other.ORDER > self.ORDER:
            if not hasattr(other, "subtract"):
                raise exceptions.ProjectorTypeError(type(other))

            return other.subtract(self)

        if other.ORDER < self.ORDER:
            if not hasattr(other, "to_abacus"):
                raise exceptions.ProjectorTypeError(type(other))

            other = other.to_abacus()

        return AbacusValue(self.raw_value - other.raw_value)

    def multiply(self, other):
        if other.ORDER > self.ORDER:
            if not hasattr(other, "multiply"):
                raise exceptions.ProjectorTypeError(type(other))

            return other.multiply(self)

        if other.ORDER < self.ORDER:
            if not hasattr(other, "to_abacus"):
                raise exceptions.ProjectorTypeError(type(other))

            other = other.to_abacus()

        return AbacusValue(self.raw_value * other.raw_value)

    def divide(self, other):
        if other.ORDER > self.ORDER:
            if not hasattr(other, "divide"):
                raise exceptions.ProjectorTypeError(type(other))

            return other.divide(self)

        if other.ORDER < self.ORDER:
            if not hasattr(other, "to_abacus"):
                raise exceptions.ProjectorTypeError(type(other))

            other = other.to_abacus()

        if not other.raw_value:
            raise exceptions.ProjectorDivisionByZeroError

        return AbacusValue(self.raw_value / other.raw_value)

    def modulo(self, other):
        if other.ORDER > self.ORDER:
            if not hasattr(other, "modulo"):
                raise exceptions.ProjectorTypeError(type(other))

            return other.modulo(self)

        if other.ORDER < self.ORDER:
            if not hasattr(other, "to_abacus"):
                raise exceptions.ProjectorTypeError(type(other))

            other = other.to_abacus()

        if not other.raw_value:
            raise exceptions.ProjectorDivisionByZeroError

        return AbacusValue(self.raw_value % other.raw_value)


class RationalValue(Value):
    DEFAULT_VALUE = 0.0
    ORDER = 3

    def __init__(self, initial_value=DEFAULT_VALUE):
        super().__init__(initial_value)

        self._signature_value_type = "Rational"

    def to_abacus(self):
        return AbacusValue(int(self.raw_value))

    def to_rational(self):
        return self

    def to_lever(self):
        return LeverValue(bool(self.raw_value))


class LeverValue(Value):
    DEFAULT_VALUE = False
    ORDER = 1

    def __init__(self, initial_value=DEFAULT_VALUE):
        super().__init__(initial_value)

        self._signature_value_type = "Lever"

    def to_abacus(self):
        return AbacusValue(int(self.raw_value))

    def to_rational(self):
        return RationalValue(int(self.raw_value))

    def to_lever(self):
        return self


class ScrollValue(Value):
    DEFAULT_VALUE = ""
    ORDER = 0

    def __init__(self, initial_value=DEFAULT_VALUE):
        super().__init__(initial_value)

        self._signature_value_type = "Scroll"

    def to_lever(self):
        return LeverValue(bool(self.raw_value))

    def to_scroll(self):
        return self
