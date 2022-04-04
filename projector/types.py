from projector import exceptions


class Value:
    # (Temporary until I properly document this)
    #
    # DEFAULT_VALUE -- the default (or null) value of this type.
    #
    # CONVERSION_SIGNATURE (default: to_<type_name_in_lowercase>) -- the name
    # of the function used to convert a value to this type
    #
    # FAMILY -- the name of the type family of this type (values of different
    # type families can't be implicitly converted into one another)
    #
    # ORDER (default: 0) -- the conversion order of this type inside its
    # family. The greater the order, the "bigger" a value is considered to be.
    # When performing operations between values of distinct types of the same
    # family, the type with the smaller order will be promoted to the type of
    # greater order.

    DEFAULT_VALUE = None
    CONVERSION_SIGNATURE = "to_null"
    FAMILY = "Null"
    ORDER = 0

    def __init__(self, initial_value=DEFAULT_VALUE):
        self._signature_value_type = "Null"

        self.raw_value = initial_value

    def __repr__(self):
        return f"<Value: {self._signature_value_type}>"

    def __str__(self):
        return str(self.raw_value)

    def implicit_promote(self, other):
        if other.FAMILY != self.FAMILY:
            raise exceptions.TypeError(repr(other))

        if other.ORDER > self.ORDER:
            if not hasattr(self, other.CONVERSION_SIGNATURE):
                raise exceptions.TypeError(repr(self))

            return getattr(self, other.CONVERSION_SIGNATURE)(), other
        elif other.ORDER < self.ORDER:
            if not hasattr(other, self.CONVERSION_SIGNATURE):
                raise exceptions.TypeError(repr(other))

            return self, getattr(other, self.CONVERSION_SIGNATURE)()

        return self, other

    def operate(self, other, operation_function, operation_name):
        first, second = self.implicit_promote(other)

        if type(first) == type(self):
            return type(self)(
                operation_function(first.raw_value, second.raw_value)
            )

        if not hasattr(first, operation_name):
            raise exceptions.TypeError(repr(first))

        return first.operate(second, operation_function, operation_name)

    def to_lever(self):
        return LeverValue(False)


class AbacusValue(Value):
    DEFAULT_VALUE = 0
    CONVERSION_SIGNATURE = "to_abacus"
    FAMILY = "Integer"
    ORDER = 0

    def __init__(self, initial_value=DEFAULT_VALUE):
        super().__init__(initial_value)

        self._signature_value_type = "Abacus"

    def to_rational(self):
        return RationalValue(float(self.raw_value))

    def to_lever(self):
        return LeverValue(bool(self.raw_value))

    def add(self, other):
        return self.operate(other, lambda x, y: x + y, "add")

    def subtract(self, other):
        return self.operate(other, lambda x, y: x - y, "subtract")

    def multiply(self, other):
        return self.operate(other, lambda x, y: x * y, "multiply")

    def divide(self, other):
        return self.operate(other, lambda x, y: x // y, "divide")

    def modulo(self, other):
        return self.operate(other, lambda x, y: x % y, "modulo")


class RationalValue(Value):
    DEFAULT_VALUE = 0.0
    CONVERSION_SIGNATURE = "to_rational"
    FAMILY = "Floating"
    ORDER = 0

    def __init__(self, initial_value=DEFAULT_VALUE):
        super().__init__(initial_value)

        self._signature_value_type = "Rational"

    def to_abacus(self):
        return AbacusValue(int(self.raw_value))

    def to_lever(self):
        return LeverValue(bool(self.raw_value))

    def add(self, other):
        return self.operate(other, lambda x, y: x + y, "add")

    def subtract(self, other):
        return self.operate(other, lambda x, y: x - y, "subtract")

    def multiply(self, other):
        return self.operate(other, lambda x, y: x * y, "multiply")

    def divide(self, other):
        return self.operate(other, lambda x, y: x // y, "divide")


class LeverValue(Value):
    DEFAULT_VALUE = False
    CONVERSION_SIGNATURE = "to_lever"
    FAMILY = "Logical"
    ORDER = 0

    def __init__(self, initial_value=DEFAULT_VALUE):
        super().__init__(initial_value)

        self._signature_value_type = "Lever"

    def to_abacus(self):
        return AbacusValue(int(self.raw_value))

    def to_rational(self):
        return RationalValue(int(self.raw_value))


class ScrollValue(Value):
    DEFAULT_VALUE = ""
    CONVERSION_SIGNATURE = "to_scroll"
    FAMILY = "Textual"
    ORDER = 0

    def __init__(self, initial_value=DEFAULT_VALUE):
        super().__init__(initial_value)

        self._signature_value_type = "Scroll"

    def to_lever(self):
        return LeverValue(bool(self.raw_value))


class ChestValue(Value):
    DEFAULT_VALUE = []
    CONVERSION_SIGNATURE = "to_chest"
    FAMILY = "Sequential"
    ORDER = 0

    def __init__(self, initial_value=[]):
        super().__init__(initial_value)

        self._signature_value_type = "Chest"

    def to_lever(self):
        return LeverValue(bool(self.raw_value))
