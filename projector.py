DIGITS = "0123456789"

SMALLEST_PRECEDENCE = 1
BIGGEST_PRECEDENCE = 5




class ProjectorError(Exception):
    def __str__(self):
        return "Unknown error"


class InvalidSymbolError(ProjectorError):
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return f"Invalid symbol '{self.symbol}'"


class InvalidOperatorSignature(ProjectorError):
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return f"Invalid operator signature '{self.symbol}'"


class UnmatchedParenthesesError(ProjectorError):
    def __init__(self, opening_index):
        self.opening_index = opening_index

    def __str__(self):
        return f"Unmatched parentheses at {self.opening_index}"


class ValueAbsentError(ProjectorError):
    def __str__(self):
        return "Expected value"


class OperatorAbsentError(ProjectorError):
    def __str__(self):
        return "Expected operator after value"



class Token:
    def __str__(self):
        return "<Token: NUL>"


class ValueToken(Token):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"<Token: VAL> {self.value}"


class OperatorToken(Token):
    def __init__(self, symbol):
        self.symbol = symbol

        match symbol:
            case '*': self.precedence = 5
            case '/': self.precedence = 4
            case '-': self.precedence = 3
            case '+': self.precedence = 2
            case '=': self.precedence = 1
            case _: self.precedence = 0

    def __str__(self):
        return f"<Token: OP> {self.symbol}"


class TokenGroup(Token):
    def __init__(self, token_list = []):
        self.token_list = token_list
        self.operative, self.nested = get_token_list_attributes(token_list)

    def __len__(self):
        return len(self.token_list)

    def __getitem__(self, key):
        return self.token_list[key]

    def __str__(self, indent_level=0):
        hash_signature = str(hash(self))
        indent_padding = indent_level * '\t'

        group_string = f"{indent_padding}<Token: GRP -- {hash_signature}"

        if self.operative: group_string += " (operative)"
        if self.nested: group_string += " (nested)"

        for token in self.token_list:
            if isinstance(token, TokenGroup):
                subgroup_string = token.__str__(indent_level + 1)
                group_string += f"\n{subgroup_string}"
            else:
                group_string += f"\n{indent_padding}\t{str(token)}"

        group_string += f"\n{indent_padding}{hash_signature} -- >"

        return group_string


class IntegerToken(ValueToken):
    def __init__(self, value):
        super().__init__(int(value))

    def __str__(self):
        return f"<Token: INT> {self.value}"


class OperatorAddToken(OperatorToken):
    def __init__(self):
        super().__init__('+')


class OperatorSubToken(OperatorToken):
    def __init__(self):
        super().__init__('-')


class OperatorMulToken(OperatorToken):
    def __init__(self):
        super().__init__('*')


class OperatorDivToken(OperatorToken):
    def __init__(self):
        super().__init__('/')


class OperatorAssignToken(OperatorToken):
    def __init__(self):
        super().__init__('=')



class ValueExpression:
    def __init__(self, value_token):
        self.value_token = value_token

    def evaluate(self):
        return self.value_token.value


class OperationExpression:
    def __init__(self, operator_token, left=None, right=None):
        self.operator_token = operator_token
        self.left = left
        self.right = right

    def evaluate(self):
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()

        match self.operator_token.symbol:
            case '*': return left_value * right_value
            case '/': return left_value / right_value
            case '+': return left_value + right_value
            case '-': return left_value - right_value
            case _: raise InvalidOperatorSignature(self.operator_token.symbol)




def get_next_operator_index(token_group):
    operator_precedence = BIGGEST_PRECEDENCE + 1
    operator_index = -1

    index = len(token_group) - 1
    for token in list(reversed(token_group.token_list)):
        if isinstance(token, OperatorToken) and \
                token.precedence < operator_precedence:
            operator_index = index
            operator_precedence = token.precedence

            if token.precedence == SMALLEST_PRECEDENCE: break

        index -= 1

    return operator_index


def get_token_list_attributes(token_list):
    operative = False
    nested = False

    for token in token_list:
        if isinstance(token, OperatorToken): operative = True
        elif isinstance(token, TokenGroup): nested = True

        if operative and nested: break

    return operative, nested


def extract_integer(expression, starting_index):
    number_string = expression[starting_index]

    if starting_index < len(expression) - 1:
        for character in expression[starting_index + 1 :]:
            if character not in DIGITS: break

            number_string += character

    return number_string


def extract_group(expression, opening_index):
    if opening_index == len(expression) - 1:
        raise UnmatchedParenthesesError(opening_index)

    closing_index = expression.rfind(')', opening_index + 1)

    if closing_index == -1:
        raise UnmatchedParenthesesError(opening_index)

    token_list = tokenize(expression[opening_index + 1 : closing_index])

    return TokenGroup(token_list), closing_index



def tokenize(expression):
    token_list = []

    index = 0
    while index < len(expression):
        if expression[index] in DIGITS:
            number_string = extract_integer(expression, index)
            index += len(number_string) - 1
            token_list.append(IntegerToken(number_string))
        else:
            match expression[index]:
                case '(':
                    token_group, index = extract_group(expression, index)
                    token_list.append(token_group)
                case '+':
                    token_list.append(OperatorAddToken())
                case '-':
                    token_list.append(OperatorSubToken())
                case '*':
                    token_list.append(OperatorMulToken())
                case '/':
                    token_list.append(OperatorDivToken())
                case '=':
                    token_list.append(OperatorAssignToken())
                case _:
                    raise InvalidSymbolError(expression[index])

        index += 1

    return token_list


def parse(token):
    if isinstance(token, ValueToken):
        return ValueExpression(token)
    elif isinstance(token, OperatorToken):
        return OperationExpression(token)

    if not token:
        raise ValueAbsentError

    if not token.operative:
        if len(token) > 1: raise OperatorAbsentError

        return parse(token.token_list[0])

    operator_index = get_next_operator_index(token)

    if operator_index == 0 or operator_index == len(token) - 1:
        raise ValueAbsentError

    left_tokens = token[: operator_index]
    right_tokens = token[operator_index + 1 :]

    return OperationExpression(
        token.token_list[operator_index],
        parse(TokenGroup(left_tokens)),
        parse(TokenGroup(right_tokens))
    )


def main():
    try:
        input_expression = input("ProjectOr expression: ").replace(' ', '')
        token_list = tokenize(input_expression)
        parsed_expression = parse(TokenGroup(token_list))
        print(f"ProjectOr result: {parsed_expression.evaluate()}")
    except ProjectorError as ex:
        print(ex)


if __name__ == "__main__":
    main()
