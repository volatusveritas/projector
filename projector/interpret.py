from projector import constants
from projector import exceptions
from projector import expressions
from projector import tokens


def get_next_operator_index(token_list):
    operator_precedence = constants.BIGGEST_PRECEDENCE + 1
    operator_index = -1

    index = len(token_list) - 1
    for token in list(reversed(token_list)):
        if (
            isinstance(token, tokens.OperatorToken)
            and token.precedence < operator_precedence
        ):
            operator_index = index
            operator_precedence = token.precedence

            if token.precedence == constants.SMALLEST_PRECEDENCE:
                break

        index -= 1

    return operator_index


def extract_word(expression, starting_index):
    if starting_index == len(expression) - 1:
        return expression[starting_index], starting_index

    ending_index = starting_index

    for character in expression[starting_index + 1 :]:
        if character not in constants.WORD_CHARACTERS:
            break

        ending_index += 1

    return expression[starting_index : ending_index + 1], ending_index


def extract_number(expression, starting_index):
    if starting_index == len(expression) - 1:
        return expression[starting_index], False, starting_index

    ending_index = starting_index
    is_float = False

    for character in expression[starting_index + 1 :]:
        if character == ".":
            if is_float:
                break
            is_float = True
        elif character not in constants.DECIMAL_NUMBER_CHARACTERS:
            break

        ending_index += 1

    return (
        expression[starting_index : ending_index + 1],
        is_float,
        ending_index,
    )


def extract_string(expression, opening_index):
    if opening_index == len(expression) - 1:
        raise exceptions.UnmatchedQuotesError

    closing_index = expression.find('"', opening_index + 1)

    if closing_index == -1:
        raise exceptions.UnmatchedQuotesError

    return expression[opening_index + 1 : closing_index], closing_index


def tokenize_unitoken(character):
    match character:
        case "+":
            return tokens.AdditionToken()
        case "-":
            return tokens.SubtractionToken()
        case "*":
            return tokens.MultiplicationToken()
        case "/":
            return tokens.DivisionToken()
        case "%":
            return tokens.ModuloToken()
        case "=":
            return tokens.AssignmentToken()
        case ",":
            return tokens.CommaToken()
        case "(":
            return tokens.ParenthesesToken(False)
        case ")":
            return tokens.ParenthesesToken(True)
        case "[":
            return tokens.BracketsToken(False)
        case "]":
            return tokens.BracketsToken(True)
        case "{":
            return tokens.BracesToken(False)
        case "}":
            return tokens.BracesToken(True)
        case "<":
            return tokens.ChevronsToken(False)
        case ">":
            return tokens.ChevronsToken(True)
        case _:
            raise exceptions.InvalidSymbolError(character)


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
        elif raw_expression[index] in constants.DECIMAL_NUMBER_CHARACTERS:
            number_str, is_float, index = extract_number(raw_expression, index)
            if is_float:
                token_list.append(tokens.FloatToken(float(number_str)))
            else:
                token_list.append(tokens.IntegerToken(int(number_str)))
        elif raw_expression[index] in constants.WORD_BEGIN_CHARACTERS:
            word_str, index = extract_word(raw_expression, index)
            token_list.append(tokenize_word(word_str))
        else:
            token_list.append(tokenize_unitoken(raw_expression[index]))

        index += 1

    return token_list


def parse(token_list):
    if not token_list:
        return expressions.Expression()

    operator_index = get_next_operator_index(token_list)

    if operator_index == -1:
        if len(token_list) > 1:
            raise exceptions.OperatorAbsentError

        return token_list[0].getexpr()

    before_operator = token_list[:operator_index]
    after_operator = token_list[operator_index:]
    del after_operator[0]

    return token_list[operator_index].getexpr(
        parse(before_operator), parse(after_operator)
    )


def evaluate_single(raw_expression, debug_mode=False, tokenizer_only=False):
    try:
        token_list = tokenize(raw_expression)

        if tokenizer_only:
            for token in token_list:
                print(token)

            return None

        expression = parse(token_list)
        return expression.evaluate()
    except exceptions.Error as error:
        if debug_mode:
            raise error

        print(error)


def evaluate(raw_expression, debug_mode=False, tokenizer_only=False):
    for raw_subexpression in raw_expression.split(";"):
        return evaluate_single(raw_subexpression, debug_mode, tokenizer_only)
