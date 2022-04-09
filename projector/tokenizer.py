from projector.constants import *
from projector import exceptions
from projector import tokens


class Tokenizer:
    def start(self, input_str, idx=0):
        self.string = input_str
        self.idx = idx
        self.last_was_value = False
        self.token_list = []
        self.current = input_str[idx]

    def tokenize(self):
        while self.idx < len(self.string):
            self.tokenize_next()

            self.idx += 1
            self.current = self.string[self.idx]

        return self.token_list

    def tokenize_next(self):
        if self.current in WHITESPACE_CHARACTERS:
            return

        if self.current in STRING_DELIMITERS:
            self.token_list.append(tokens.Scroll(self.extract_string()))
        elif self.current in WORD_BEGIN_CHARACTERS:
            self.tokenize_word()
        elif self.current in DECIMAL_CHARACTERS:
            self.tokenize_number()
        else:
            self.tokenize_unitoken()

    def tokenize_word(self):
        word = self.extract_word()

        if word in FLOWSTOP_KEYWORDS:
            self.last_was_value = False
            self.token_list.append(tokens.Break())
        else:
            match word:
                case "on":
                    self.token_list.append(tokens.Lever(True))
                case "off":
                    self.token_list.append(tokens.Lever(False))
                case _:
                    self.token_list.append(tokens.Identifier(word))

            self.last_was_value = True

    def tokenize_number(self):
        number_str, is_float = self.extract_number(negative=False)

    def tokenize_unitoken(self):
        match self.current:
            case "+":
                self.token_list.append(tokens.Addition())
            case "-":
                if self.last_was_value:
                    self.token_list.append(tokens.Negation())
                elif (
                    self.idx < len(self.string) - 1
                    and self.string[self.idx + 1] in DECIMAL_CHARACTERS
                ):
                    pass
                self.token_list.append(tokens.Subtraction())
            case "*":
                self.token_list.append(tokens.Multiplication())
            case "/":
                self.token_list.append(tokens.Division())
            case "%":
                self.token_list.append(tokens.Modulo())
            case "=":
                self.token_list.append(tokens.Assignment())
            case ",":
                self.token_list.append(tokens.Comma())
            case "(":
                self.token_list.append(tokens.Parentheses(False))
            case ")":
                self.token_list.append(tokens.Parentheses(True))
            case "[":
                self.token_list.append(tokens.Brackets(False))
            case "]":
                self.token_list.append(tokens.Brackets(True))
            case "{":
                self.token_list.append(tokens.Braces(False))
            case "}":
                self.token_list.append(tokens.Braces(True))
            case "<":
                self.token_list.append(tokens.Chevrons(False))
            case ">":
                self.token_list.append(tokens.Chevrons(True))
            case _:
                raise exceptions.InvalidSymbolError(self.current)

    def extract_number(self, negative):
        if self.idx == len(self.string) - 1:
            self.last_was_value = True
            return self.string[self.idx]

        start_idx = self.idx
        end_idx = self.idx
        is_float = False

        for character in self.string[start_idx + 1 :]:
            if character == ".":
                if is_float:
                    break

                is_float = True
            elif character not in DECIMAL_CHARACTERS:
                break

            end_idx += 1

        return "-"*negative + self.string[start_idx : end_idx + 1], is_float

    def extract_string(self):
        if self.idx == len(self.string) - 1:
            raise exceptions.UnmatchedQuotesError

        open_idx = self.idx
        close_idx = self.string.find(self.string[open_idx], open_idx + 1)

        if close_idx == -1:
            raise exceptions.UnmatchedQuotesError

        self.idx = close_idx
        self.last_was_value = True

        return self.string[open_idx + 1 : close_idx]

    def extract_word(self):
        if self.idx == len(self.string) - 1:
            return self.string[self.idx]

        start_idx = self.idx
        end_idx = self.idx

        for character in self.string[start_idx + 1 :]:
            if character not in WORD_CHARACTERS:
                break

            end_idx += 1

        self.idx = end_idx

        return self.string[start_idx : end_idx + 1]
