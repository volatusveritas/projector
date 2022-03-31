from projector import constants
from projector import exceptions
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


def extract_string(expression, opening_index):
    if opening_index == len(expression) - 1:
        raise exceptions.ProjectorUnmatchedQuotesError

    closing_index = expression.find('"', opening_index + 1)

    if closing_index == -1:
        raise exceptions.ProjectorUnmatchedQuotesError

    return expression[opening_index + 1 : closing_index], closing_index



def tokenize_unitoken(character):
    match character:
        case '+':
            return tokens.AdditionToken()
        case '-':
            return tokens.SubtractionToken()
        case '*':
            return tokens.MultiplicationToken()
        case '/':
            return tokens.DivisionToken()
        case '%':
            return tokens.ModuloToken()
        case '=':
            return tokens.AssignmentToken()
        case _:
            raise exceptions.ProjectorInvalidSymbolError(character)


def tokenize_word(word):
    if word in constants.FLOWSTOP_KEYWORDS:
        return tokens.BreakToken()
    elif word == "on":
        return tokens.BoolToken(True)
    elif word == "off":
        return tokens.BoolToken(False)
    else:
        return tokens.IdentifierToken(word)


def tokenize(raw_expression):
    token_list = []

    index = 0
    while index < len(raw_expression):
        if raw_expression[index] in constants.WHITESPACE_CHARACTERS:
            pass
        elif raw_expression[index] == '"':
            str_value, index = extract_string(raw_expression, index)
            token_list.append(tokens.StringToken(str_value))
        elif raw_expression[index] == ',':
            token_list.append(tokens.CommaToken())
        elif raw_expression[index] == '(':
            token_list.append(tokens.ParenthesesToken(False))
        elif raw_expression[index] == ')':
            token_list.append(tokens.ParenthesesToken(True))
        elif raw_expression[index] == '[':
            token_list.append(tokens.BracketsToken(False))
        elif raw_expression[index] == ']':
            token_list.append(tokens.BracketsToken(True))
        elif raw_expression[index] == '{':
            token_list.append(tokens.BracesToken(False))
        elif raw_expression[index] == '}':
            token_list.append(tokens.BracesToken(True))
        elif raw_expression[index] == '<':
            token_list.append(tokens.ChevronsToken(False))
        elif raw_expression[index] == '>':
            token_list.append(tokens.ChevronsToken(True))
        elif raw_expression[index] in constants.DECIMAL_NUMBER_CHARACTERS:
            number_str, index = match_extraction(
                raw_expression, constants.DECIMAL_NUMBER_CHARACTERS, index
            )
            token_list.append(tokens.IntegerToken(int(number_str)))
        elif raw_expression[index] in constants.WORD_BEGIN_CHARACTERS:
            word_str, index = match_extraction(
                raw_expression, constants.WORD_CHARACTERS, index
            )
            token_list.append(tokenize_word(word_str))
        else:
            token_list.append(tokenize_unitoken(raw_expression[index]))

        index += 1

    return token_list



def parse(token):
    return token.getexpr()



def evaluate_single(raw_expression, debug_mode=False):
    try:
        token_list = tokenize(raw_expression)
        expression = parse(token_list)
        print(expression)  # temp
        # return expression.evaluate()
    except exceptions.ProjectorError as error:
        if debug_mode:
            raise error

        print(error)


def evaluate(raw_expression, debug_mode=False):
    for raw_subexpression in raw_expression.split(';'):
        evaluate_single(raw_subexpression, debug_mode)
