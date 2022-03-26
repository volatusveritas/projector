from projector import constants
from projector import exceptions
from projector import expressions
from projector import tokens




def get_next_operator_index(token_group):
    operator_precedence = constants.BIGGEST_PRECEDENCE + 1
    operator_index = -1

    index = len(token_group) - 1
    for token in list(reversed(token_group)):
        if (isinstance(token, tokens.OperatorToken) and
            token.precedence < operator_precedence
        ):
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
    if opening_index == len(expression) - 1:
        raise exceptions.ProjectorUnmatchedParenthesesError

    closing_index = expression.find(')', opening_index + 1)

    if closing_index == -1:
        raise exceptions.ProjectorUnmatchedParenthesesError

    subgroup_count = expression.count('(', opening_index + 1, closing_index)

    if subgroup_count:
        if closing_index >= len(expression) - subgroup_count:
            raise exceptions.ProjectorUnmatchedParenthesesError

        for _ in range(subgroup_count):
            closing_index = expression.find(')', closing_index + 1)

            if closing_index == -1:
                raise exceptions.ProjectorUnmatchedParenthesesError

    token_list = tokenize(expression[opening_index + 1 : closing_index])

    return tokens.TokenGroup(token_list), closing_index


def get_operator_expression_type(operator_token):
    if isinstance(operator_token, tokens.AdditionOperatorToken):
        return expressions.AdditionOperationExpression
    elif isinstance(operator_token, tokens.SubtractionOperatorToken):
        return expressions.SubtractionOperationExpression
    elif isinstance(operator_token, tokens.MultiplicationOperatorToken):
        return expressions.MultiplicationOperationExpression
    elif isinstance(operator_token, tokens.DivisionOperatorToken):
        return expressions.DivisionOperationExpression
    elif isinstance(operator_token, tokens.ModuloOperatorToken):
        return expressions.ModuloOperationExpression
    elif isinstance(operator_token, tokens.AssignmentOperatorToken):
        return expressions.AssignmentOperationExpression
    else:
        return expressions.OperationExpression



def tokenize(raw_expression):
    token_list = []

    index = 0
    while index < len(raw_expression):
        if raw_expression[index] in constants.DECIMAL_NUMBER_CHARACTERS:
            number_str, index = extract_integer(raw_expression, index)
            token_list.append(tokens.IntegerValueToken(int(number_str)))
        elif raw_expression[index] in constants.IDENTIFIER_BEGIN_CHARACTERS:
            identifier_str, index = extract_identifier(raw_expression, index)
            token_list.append(tokens.IdentifierToken(identifier_str))
        else:
            match raw_expression[index]:
                case ' ':
                    break
                case '(':
                    token_group, index = extract_group(raw_expression, index)
                    token_list.append(token_group)
                case '+':
                    token_list.append(tokens.AdditionOperatorToken())
                case '-':
                    token_list.append(tokens.SubtractionOperatorToken())
                case '*':
                    token_list.append(tokens.MultiplicationOperatorToken())
                case '/':
                    token_list.append(tokens.DivisionOperatorToken())
                case '%':
                    token_list.append(tokens.ModuloOperatorToken())
                case '=':
                    token_list.append(tokens.AssignmentOperatorToken())
                case _:
                    raise exceptions.ProjectorInvalidSymbolError(
                        raw_expression[index]
                    )

        index += 1

    return token_list



def parse_value(value_token):
    if isinstance(value_token, tokens.IntegerValueToken):
        return expressions.IntegerValueExpression(value_token)
    elif isinstance(value_token, tokens.FloatValueToken):
        return expressions.FloatValueExpression(value_token)
    elif isinstance(value_token, tokens.StringValueToken):
        return expressions.StringValueExpression(value_token)
    elif isinstance(value_token, tokens.BoolValueToken):
        return expressions.BoolValueExpression(value_token)
    else:
        return expressions.ValueExpression(value_token)


def parse_group(token_group):
    if not token_group:
        return expressions.Expression()

    if not token_group.operative:
        if len(token_group) > 1:
            raise exceptions.ProjectorOperatorAbsentError

        return parse(token_group[0])

    operator_index = get_next_operator_index(token_group)

    left_tokens = token_group[: operator_index]
    right_tokens = token_group[operator_index + 1 :]

    return get_operator_expression_type(token_group[operator_index])(
        parse_group(tokens.TokenGroup(left_tokens)),
        parse_group(tokens.TokenGroup(right_tokens))
    )


def parse(token):
    if isinstance(token, tokens.ValueToken):
        return parse_value(token)
    elif isinstance(token, tokens.OperatorToken):
        return get_operator_expression_type(token)()
    elif isinstance(token, tokens.IdentifierToken):
        return expressions.IdentifierExpression(token)
    elif isinstance(token, tokens.TokenGroup):
        return parse_group(token)
    else:
        return expressions.Expression()


def evaluate(raw_expression, debug_mode=False):
    try:
        raw_expression = " ".join(raw_expression.split())
        token_list = tokenize(raw_expression)
        expression_tree = parse(tokens.TokenGroup(token_list))
        return expression_tree.evaluate()
    except exceptions.ProjectorError as error:
        if debug_mode:
            raise error

        print(error)
