import string
import sys
import enum




IDENTIFIER_BEGIN_CHARACTERS = string.ascii_letters + '_'
IDENTIFIER_CHARACTERS = IDENTIFIER_BEGIN_CHARACTERS + string.digits

SMALLEST_PRECEDENCE = 1
BIGGEST_PRECEDENCE = 5


variable_bank = {}




class OperationType(enum.Enum):
    NONE = 0
    ADDITION = enum.auto()
    SUBTRACTION = enum.auto()
    MULTIPLICATION = enum.auto()
    DIVISION = enum.auto()
    MODULO = enum.auto()
    ASSIGNMENT = enum.auto()

    def __str__(self):
        match self.value:
            case self.ADDITION:
                return "Addition"
            case self.SUBTRACTION:
                return "Subtraction"
            case self.MULTIPLICATION:
                return "Multiplication"
            case self.DIVISION:
                return "Division"
            case self.MODULO:
                return "Modulo"
            case self.ASSIGNMENT:
                return "Assignment"
            case _:
                return "None"


class ValueType(enum.Enum):
    NONE = 0
    INTEGER = enum.auto()
    FLOATING_POINT = enum.auto()
    STRING = enum.auto()
    BOOL = enum.auto()

    def __str__(self):
        match self.value:
            case self.INTEGER:
                return "Integer"
            case self.FLOATING_POINT:
                return "Float"
            case self.STRING:
                return "String"
            case self.BOOL:
                return "Bool"
            case _:
                return "None"




class ProjectorError(Exception):
    pass



class Token:
    def __str__(self):
        return "<Token: Null>"


class ValueToken(Token):
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return f"<Token: Value> ({str(self.type)}) {self.value}"


class OperatorToken(Token):
    def __init__(self, type):
        self.type = type

        match type:
            case OperationType.MULTIPLICATION:
                self.precedence = 5
            case OperationType.DIVISION:
                self.precedence = 4
            case OperationType.MODULO:
                self.precedence = 4
            case OperationType.SUBTRACTION:
                self.precedence = 3
            case OperationType.ADDITION:
                self.precedence = 2
            case OperationType.ASSIGNMENT:
                self.precedence = 1
            case _:
                self.precedence = 0

    def __str__(self):
        return f"<Token: Operation> [{str(self.type)}]"


class IdentifierToken(Token):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"<Token: Identifier> {self.name}"


class TokenGroup(Token):
    def __init__(self, token_list = []):
        self.token_list = token_list
        self.operative, self.nested = self.get_attributes()

    def __len__(self):
        return len(self.token_list)

    def __getitem__(self, key):
        return self.token_list[key]

    def __str__(self, indent_level=0):
        hash_signature = hash(self)
        indent_padding = indent_level * '\t'

        group_string = f"{indent_padding}<Token: GRP -- {hash_signature}"

        if self.operative:
            group_string += " (operative)"

        if self.nested:
            group_string += " (nested)"

        for token in self.token_list:
            if isinstance(token, TokenGroup):
                subgroup_string = token.__str__(indent_level + 1)
                group_string += f"\n{subgroup_string}"
            else:
                group_string += f"\n{indent_padding}\t{str(token)}"

        group_string += f"\n{indent_padding}{hash_signature} -- >"

        return group_string

    def get_attributes(self):
        operative = False
        nested = False

        for token in self.token_list:
            if isinstance(token, OperatorToken):
                operative = True
            elif isinstance(token, TokenGroup):
                nested = True

            if operative and nested:
                break

        return operative, nested





class Expression:
    def __str__(self):
        return "<Expression: Null>"

    def evaluate(self):
        return None


class ValueExpression(Expression):
    def __init__(self, value_token):
        self.value = value_token.value
        self.type = value_token.type

    def __str__(self):
        return f"<Expression: Value> ({str(self.type)}) {self.value}"

    def evaluate(self):
        return self.value


class OperationExpression(Expression):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def __str__(self):
        return f"<Expression: Operation> [None]"


class IdentifierExpression(Expression):
    def __init__(self, identifier_token):
        self.name = identifier_token.name

    def __str__(self):
        return f"<Expression: Identififer> {self.name}"

    def evaluate(self):
        return variable_bank[self.name]


class OperationAddExpression(OperationExpression):
    def evaluate(self):
        left_term = self.left.evaluate()
        right_term = self.right.evaluate()

        if right_term is None:
            raise ValueAbsentError

        if left_term is None:
            left_term = 0

        return left_term + right_term


class OperationSubExpression(OperationExpression):
    def evaluate(self):
        left_term = self.left.evaluate()
        right_term = self.right.evaluate()

        if right_term is None:
            raise ValueAbsentError

        if left_term is None:
            left_term = 0

        return left_term - right_term


class OperationMulExpression(OperationExpression):
    def evaluate(self):
        left_factor = self.left.evaluate()
        right_factor = self.right.evaluate()

        if left_factor is None or right_factor is None:
            raise ValueAbsentError

        return left_factor * right_factor


class OperationDivExpression(OperationExpression):
    def evaluate(self):
        dividend = self.left.evaluate()
        divisor = self.right.evaluate()

        if dividend is None or divisor is None:
            raise ValueAbsentError

        if divisor == 0:
            raise ZeroDivisionError

        return dividend // divisor


class OperationModExpression(OperationExpression):
    def evaluate(self):
        dividend = self.left.evaluate()
        divisor = self.right.evaluate()

        if dividend is None or divisor is None:
            raise ValueAbsentError

        if not isinstance(dividend, int) or not isinstance(divisor, int):
            raise TypeError

        if divisor == 0:
            raise ZeroDivisionError

        return dividend % divisor


class OperationAssignExpression(OperationExpression):
    def evaluate(self):
        if not isinstance(self.left, IdentifierExpression):
            raise TypeError

        value = self.right.evaluate()

        if value is None:
            raise ValueAbsentError

        if not isinstance(value, (int, str)):
            raise TypeError

        variable_bank[self.left.identifier_token.name] = value

        return None




def get_next_operator_index(token_group):
    operator_precedence = BIGGEST_PRECEDENCE + 1
    operator_index = -1

    index = len(token_group) - 1
    for token in list(reversed(token_group.token_list)):
        if (isinstance(token, OperatorToken) and
                token.precedence < operator_precedence):
            operator_index = index
            operator_precedence = token.precedence

            if token.precedence == SMALLEST_PRECEDENCE:
                break

        index -= 1

    return operator_index


def match_extraction(str, matching_group, starting_index=0):
    if starting_index == len(str) - 1:
        return str[starting_index], starting_index

    ending_index = starting_index

    for character in str[starting_index + 1 :]:
        if character not in matching_group:
            break

        ending_index += 1

    return str[starting_index : ending_index + 1], ending_index


def extract_integer(expression, starting_index):
    return match_extraction(expression, string.digits, starting_index)


def extract_identifier(expression, starting_index):
    return match_extraction(expression, IDENTIFIER_CHARACTERS, starting_index)


def extract_group(expression, opening_index):
    if opening_index == len(expression) - 1:
        raise UnmatchedParenthesesError(opening_index)

    closing_index = expression.find(')', opening_index + 1)

    if closing_index == -1:
        raise UnmatchedParenthesesError(opening_index)

    subgroup_count = expression.count('(', opening_index + 1, closing_index)

    if subgroup_count:
        if closing_index == len(expression) - 1:
            raise UnmatchedParenthesesError(opening_index)

        for _ in range(subgroup_count):
            closing_index = expression.find(')', closing_index + 1)

        if closing_index == -1:
            raise UnmatchedParenthesesError(opening_index)

    token_list = tokenize(expression[opening_index + 1 : closing_index])

    return TokenGroup(token_list), closing_index


def get_operation_expression_type(operator_token):
    if isinstance(operator_token, AddOperatorToken):
        return OperationAddExpression
    elif isinstance(operator_token, SubOperatorToken):
        return OperationSubExpression
    elif isinstance(operator_token, MulOperatorToken):
        return OperationMulExpression
    elif isinstance(operator_token, DivOperatorToken):
        return OperationDivExpression
    elif isinstance(operator_token, ModOperatorToken):
        return OperationModExpression
    elif isinstance(operator_token, AssignOperatorToken):
        return OperationAssignExpression
    else:
        raise UnexpectedError



def tokenize(expression):
    token_list = []

    index = 0
    while index < len(expression):
        if expression[index] in string.digits:
            number_str, index = extract_integer(expression, index)
            token_list.append(IntegerValueToken(number_str))
        elif expression[index] in IDENTIFIER_BEGIN_CHARACTERS:
            identifier_str, index = extract_identifier(expression, index)
            token_list.append(IdentifierToken(identifier_str))
        else:
            match expression[index]:
                case '(':
                    token_group, index = extract_group(expression, index)
                    token_list.append(token_group)
                case '+':
                    token_list.append(AddOperatorToken())
                case '-':
                    token_list.append(SubOperatorToken())
                case '*':
                    token_list.append(MulOperatorToken())
                case '/':
                    token_list.append(DivOperatorToken())
                case '%':
                    token_list.append(ModOperatorToken())
                case '=':
                    token_list.append(AssignOperatorToken())
                case _:
                    raise InvalidSymbolError(expression[index])

        index += 1

    return token_list


def parse_group(token):
    if not token:
        return Expression()

    if not token.operative:
        if len(token) > 1:
            raise OperatorAbsentError

        return parse(token.token_list[0])

    operator_index = get_next_operator_index(token)

    left_tokens = token[: operator_index]
    right_tokens = token[operator_index + 1 :]

    return get_operation_expression_type(token[operator_index])(
        parse(TokenGroup(left_tokens)),
        parse(TokenGroup(right_tokens))
    )


def parse(token):
    if isinstance(token, ValueToken):
        return ValueExpression(token)
    elif isinstance(token, OperatorToken):
        return get_operation_expression_type(token)()
    elif isinstance(token, IdentifierToken):
        return IdentifierExpression(token)
    elif isinstance(token, TokenGroup):
        return parse_group(token)
    else:
        raise UnexpectedError


def evaluate(input_expression):
    input_expression = input_expression.replace(' ', '')
    token_list = tokenize(input_expression)
    parsed_expression = parse(TokenGroup(token_list))
    return parsed_expression.evaluate()



def main():
    if len(sys.argv) > 1:
        for argument in sys.argv[1 :]:
            for input_expression in argument.replace(' ', '').split(';'):
                result = evaluate(input_expression)

                if result:
                    print(result)
        return

    while True:
        input_expression = input("> ")

        if input_expression == "stop":
            break

        try:
            result = evaluate(input_expression)

            if result:
                print(f">>> {result}")
        except Exception as ex:
            print(ex)




if __name__ == "__main__":
    main()
