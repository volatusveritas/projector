import projector.constants as constants
import projector.error as error
import projector.expression as expression
import projector.token as token
import projector.varbank as varbank




def get_next_operator_index(token_group):
    operator_precedence = constants.BIGGEST_PRECEDENCE + 1
    operator_index = -1

    index = len(token_group) - 1
    for token in list(reversed(token_group)):
        if (isinstance(token, token.OperatorToken) and
                token.precedence < operator_precedence):
            operator_index = index
            operator_precedence = token.precedence

            if token.precedence == constants.SMALLEST_PRECEDENCE:
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
    return match_extraction(
        expression, constants.DECIMAL_NUMBER_CHARACTERS, starting_index
    )


def extract_identifier(expression, starting_index):
    return match_extraction(
        expression, constants.IDENTIFIER_CHARACTERS, starting_index
    )


def extract_group(expression, opening_index):
    closing_index = expression.find(')', opening_index + 1)

    subgroup_count = expression.count('(', opening_index + 1, closing_index)

    if subgroup_count:
        for _ in range(subgroup_count):
            closing_index = expression.find(')', closing_index + 1)

    token_list = tokenize(expression[opening_index + 1 : closing_index])

    return token.TokenGroup(token_list), closing_index


def get_operator_expression_type(operator_token):
    if isinstance(operator_token, token.AdditionOperatorToken):
        return expression.AdditionOperationExpression
    elif isinstance(operator_token, token.SubtractionOperatorToken):
        return expression.SubtractionOperationExpression
    elif isinstance(operator_token, token.MultiplicationOperatorToken):
        return expression.MultiplicationOperationExpression
    elif isinstance(operator_token, token.DivisionOperatorToken):
        return expression.DivisionOperationExpression
    elif isinstance(operator_token, token.ModuloOperatorToken):
        return expression.ModuloOperationExpression
    elif isinstance(operator_token, token.AssignmentOperatorToken):
        return expression.AssignmentOperationExpression
    else:
        return expression.OperationExpression



def tokenize(raw_expression):
    token_list = []

    index = 0
    while index < len(raw_expression):
        if raw_expression[index] in constants.DECIMAL_NUMBER_CHARACTERS:
            number_str, index = extract_integer(raw_expression, index)
            token_list.append(token.IntegerValueToken(int(number_str)))
        elif raw_expression[index] in constants.IDENTIFIER_BEGIN_CHARACTERS:
            identifier_str, index = extract_identifier(raw_expression, index)
            token_list.append(token.IdentifierToken(identifier_str))
        else:
            match raw_expression[index]:
                case '(':
                    token_group, index = extract_group(raw_expression, index)
                    token_list.append(token_group)
                case '+':
                    token_list.append(token.AdditionOperatorToken())
                case '-':
                    token_list.append(token.SubtractionOperatorToken())
                case '*':
                    token_list.append(token.MultiplicationOperatorToken())
                case '/':
                    token_list.append(token.DivisionOperatorToken())
                case '%':
                    token_list.append(token.ModuloOperatorToken())
                case '=':
                    token_list.append(token.AssignmentOperatorToken())

        index += 1

    return token_list



def parse_value(value_token):
    if isinstance(value_token, value_token.IntegerValueToken):
        return expression.IntegerValueExpression(value_token)
    elif isinstance(value_token, value_token.FloatValueToken):
        return expression.FloatValueExpression(value_token)
    elif isinstance(value_token, value_token.StringValueToken):
        return expression.StringValueExpression(value_token)
    elif isinstance(value_token, value_token.BoolValueToken):
        return expression.BoolValueExpression(value_token)
    else:
        return expression.ValueExpression(value_token)


def parse_group(token_group):
    if not token_group:
        return expression.Expression()

    if not token_group.operative:
        return parse(token_group.token_list[0])

    operator_index = get_next_operator_index(token_group)

    left_tokens = token_group[: operator_index]
    right_tokens = token_group[operator_index + 1 :]

    return get_operator_expression_type(token_group[operator_index])(
        parse_group(token.TokenGroup(left_tokens)),
        parse_group(token.TokenGroup(right_tokens))
    )


def parse(token):
    if isinstance(token, token.ValueToken):
        return parse_value(token)
    elif isinstance(token, token.OperatorToken):
        return get_operator_expression_type(token)()
    elif isinstance(token, token.IdentifierToken):
        return expression.IdentifierExpression(token)
    elif isinstance(token, token.TokenGroup):
        return parse_group(token)
    else:
        return expression.Expression()


def execute(expression):
    variable_bank = varbank.VariableBank()

    if isinstance(expression, expression.IdentifierExpression):
        return expression.evaluate(variable_bank)
    else:
        return expression.evaluate()


def evaluate(raw_expression):
    raw_expression = "".join(raw_expression.split())
    token_list = tokenize(raw_expression)
    expression_tree = parse(token.TokenGroup(token_list))
    return execute(expression_tree)
