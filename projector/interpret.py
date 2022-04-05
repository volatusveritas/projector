from projector import constants
from projector import exceptions
from projector import expressions
from projector import tokens
from projector import types


def get_next_operator_index(token_list):
    operator_precedence = constants.BIGGEST_PRECEDENCE + 1
    operator_index = -1

    index = len(token_list) - 1
    for token in list(reversed(token_list)):
        if (
            isinstance(token, tokens.Operator)
            and token.precedence < operator_precedence
        ):
            operator_index = index
            operator_precedence = token.precedence

            if token.precedence == constants.SMALLEST_PRECEDENCE:
                break

        index -= 1

    return operator_index


def extract_number(expression, starting_index, negative):
    if starting_index == len(expression) - 1:
        return expression[starting_index], False, starting_index

    ending_index = starting_index
    is_float = False

    for character in expression[starting_index + 1 :]:
        if character == ".":
            if is_float:
                break
            is_float = True
        elif character not in constants.DECIMAL_CHARACTERS:
            break

        ending_index += 1

    return (
        ("-" * negative) + expression[starting_index : ending_index + 1],
        is_float,
        ending_index,
    )


def tokenize(raw_expression):
    if raw_expression[index] in constants.DECIMAL_CHARACTERS:
        number_str, is_float, index = extract_number(
            raw_expression, index, False
        )
        if is_float:
            token_list.append(
                tokens.RationalToken(
                    types.RationalValue(float(number_str))
                )
            )
        else:
            token_list.append(
                tokens.AbacusToken(types.AbacusValue(int(number_str)))
            )
    elif (
        raw_expression[index] == "-"
        and index < len(raw_expression) - 1
        and raw_expression[index + 1] in constants.DECIMAL_CHARACTERS
    ):
        number_str, is_float, index = extract_number(
            raw_expression, index + 1, True
        )
        if is_float:
            token_list.append(
                tokens.RationalToken(
                    types.RationalValue(-float(number_str))
                )
            )
        else:
            token_list.append(
                tokens.AbacusToken(types.AbacusValue(-int(number_str)))
            )

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
    except Exception as error:
        if debug_mode:
            raise error

        print(error)


def evaluate(raw_expression, debug_mode=False, tokenizer_only=False):
    for raw_subexpression in raw_expression.split(";"):
        return evaluate_single(raw_subexpression, debug_mode, tokenizer_only)
