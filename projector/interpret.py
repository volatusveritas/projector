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



def tokenize_unitoken(character):
    match character:
        case '+':
            return tokens.AdditionOperatorToken()
        case '-':
            return tokens.SubtractionOperatorToken()
        case '*':
            return tokens.MultiplicationOperatorToken()
        case '/':
            return tokens.DivisionOperatorToken()
        case '%':
            return tokens.ModuloOperatorToken()
        case '=':
            return tokens.AssignmentOperatorToken()
        case _:
            raise exceptions.ProjectorInvalidSymbolError(character)


def tokenize_word(word):
    if word in constants.FLOWSTOP_KEYWORDS:
        return tokens.BreakFlowToken()
    else:
        return tokens.IdentifierToken(word)


def tokenize(raw_expression):
    token_list = []

    index = 0
    while index < len(raw_expression):
        if raw_expression[index] == ' ':
            pass
        elif raw_expression[index] == '(':
            token_group, index = extract_group(raw_expression, index)
            token_list.append(token_group)
        elif raw_expression[index] in constants.DECIMAL_NUMBER_CHARACTERS:
            number_str, index = match_extraction(
                raw_expression, constants.DECIMAL_NUMBER_CHARACTERS, index
            )
            token_list.append(tokens.IntegerValueToken(int(number_str)))
        elif raw_expression[index] in constants.WORD_BEGIN_CHARACTERS:
            word_str, index = match_extraction(
                raw_expression, constants.WORD_CHARACTERS, index
            )
            token_list.append(tokenize_word(word_str))
        else:
            token_list.append(tokenize_unitoken(raw_expression[index]))

        index += 1

    return token_list



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

    return token_group[operator_index].getexpr(
        parse_group(tokens.TokenGroup(left_tokens)),
        parse_group(tokens.TokenGroup(right_tokens))
    )


def parse(token):
    if isinstance(token, tokens.TokenGroup):
        return parse_group(token)

    return token.getexpr()


def evaluate(raw_expression, debug_mode=False):
    try:
        token_list = tokenize(" ".join(raw_expression.split()))
        expression = parse(tokens.TokenGroup(token_list))
        return expression.evaluate()
    except exceptions.ProjectorError as error:
        if debug_mode:
            raise error

        print(error)
