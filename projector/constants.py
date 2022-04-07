from string import ascii_letters, digits


# Operator Precedence
SMALLEST_PRECEDENCE: int = 1
ASSIGNMENT_PRECEDENCE: int = 1
ADDITION_PRECEDENCE: int = 2
SUBTRACTION_PRECEDENCE: int = 2
MULTIPLICATION_PRECEDENCE: int = 3
DIVISION_PRECEDENCE: int = 3
MODULO_PRECEDENCE: int = 3
BIGGEST_PRECEDENCE: int = 3

# Token Masks
STRING_DELIMITERS: str = "\"'"
WHITESPACE_CHARACTERS: str = " \f\n\r\t\v"
WORD_BEGIN_CHARACTERS: str = ascii_letters + "_"
WORD_CHARACTERS: str = WORD_BEGIN_CHARACTERS + digits
DECIMAL_CHARACTERS: str = digits
FLOWSTOP_KEYWORDS: list[str] = ["exit", "stop", "quit"]

# Defaults
ABSENT_SYMBOL_NAME: str = "<unknown>"
