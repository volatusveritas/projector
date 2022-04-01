from string import ascii_letters, digits

from projector import types




# Operator Precedence
SMALLEST_PRECEDENCE = 1
ASSIGNMENT_PRECEDENCE = 1
ADDITION_PRECEDENCE = 2
SUBTRACTION_PRECEDENCE = 2
MULTIPLICATION_PRECEDENCE = 3
DIVISION_PRECEDENCE = 3
MODULO_PRECEDENCE = 3
BIGGEST_PRECEDENCE = 3

# Token Masks
WHITESPACE_CHARACTERS = " \f\n\r\t\v"
WORD_BEGIN_CHARACTERS = ascii_letters + '_'
WORD_CHARACTERS = WORD_BEGIN_CHARACTERS + digits
DECIMAL_NUMBER_CHARACTERS = digits
FLOWSTOP_KEYWORDS = ["exit", "stop", "quit"]

# Defaults
ABSENT_SYMBOL_NAME = "<unknown>"

# Typegroups
NUMERICAL_TYPES = (types.AbacusValue,)
VALUE_TYPES = NUMERICAL_TYPES + (types.ScrollValue,)
