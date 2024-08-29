from dataclasses import dataclass
from pathlib import Path
import re


class JackFileCleaner:
    """
    The auxiliary class for removing single and multi line comments and empty lines from Jack files
    It prepares list of clear Jack code lines without comments and empty lines
    """
    REGEXP_MULTILINE_COMMIT = re.compile("(/\\*{1,2}.*?\\*/)", flags=re.S | re.M)
    REGEXP_SINGLE_LINE_COMMIT = re.compile("//.*$", flags=re.M)

    def __init__(self, file: Path):
        self.file = file

    def clean_file_from_comments_and_white_spaces_and_return_code_lines(self) -> list:
        with open(self.file) as file:
            data = file.read()
        return self._remove_white_spaces_and_convert_to_list(self._remove_comments(data))

    @staticmethod
    def _remove_white_spaces_and_convert_to_list(file_context: str) -> list:
        return [line.strip() for line in file_context.splitlines() if line]

    @staticmethod
    def _remove_comments(file_context: str) -> str:
        file_context = JackFileCleaner.REGEXP_MULTILINE_COMMIT.sub("", file_context)
        return JackFileCleaner.REGEXP_SINGLE_LINE_COMMIT.sub("", file_context)


class JackTokenizer:
    KEYWORDS = {
        'class', 'constructor', 'function', 'method', 'field', 'static',
        'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
        'this', 'let', 'do', 'if', 'else', 'while', 'return',
    }
    SYMBOLS = {
        '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
        '&', '|', '<', '>', '=', '~',
    }
    # SYMBOLS_REGEXP = re.compile("([{}()[].,;+-*/&|<>=~])")
    SYMBOLS_REGEXP = re.compile("(\{|\}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||\<|\>|\=|\~)")
    INT_MIN = 0
    INT_MAX = 32767

    def __init__(self, jack_file: Path):
        self.index = 0
        self.jack_file = jack_file
        self.jack_code_lines = JackFileCleaner(jack_file).\
            clean_file_from_comments_and_white_spaces_and_return_code_lines()
        # self.jack_tokenizer_generator = self._generator()
        self.tokens = self._create_all_tokens_list_without_category()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __iter__(self):
        return self

    def _create_all_tokens_list_without_category(self):
        tokens = []
        for jack_line in self.jack_code_lines:
            lines_split_by_symbols = JackTokenizer.SYMBOLS_REGEXP.split(jack_line)
            for token in lines_split_by_symbols:
                if token:
                    # is token a string constant
                    if token.startswith('"') and token.endswith('"'):
                        tokens.append(token)
                    else:
                        # split tokens by whitespace if not a string constant
                        for single_token in token.split():
                            tokens.append(single_token)
        return tokens

    def move_backward(self):
        if self.index > -1:
            self.index -= 1

    def _generator(self):
        for token in self._create_all_tokens_list_without_category():
            if token in JackTokenizer.KEYWORDS:
                yield Token('KEYWORD', token)
            elif token in JackTokenizer.SYMBOLS:
                yield Token('SYMBOL', token)
            elif token.isnumeric():
                if JackTokenizer.INT_MIN <= int(token) <= JackTokenizer.INT_MAX:
                    yield Token('INT_CONST', int(token))
            elif token.startswith('"') and token.endswith('"'):
                yield Token('STRING_CONST', token)
            else:
                yield Token('IDENTIFIER', token)

    def has_more_tokens(self):
        pass

    def __next__(self):
        if self.index >= len(self.tokens):
            raise StopIteration
        token = self.tokens[self.index]
        self.index += 1
        return self.parse_token(token)

    @staticmethod
    def parse_token(token):
        if token in JackTokenizer.KEYWORDS:
            return Token('KEYWORD', token)
        elif token in JackTokenizer.SYMBOLS:
            return Token('SYMBOL', token)
        elif token.isnumeric():
            if JackTokenizer.INT_MIN <= int(token) <= JackTokenizer.INT_MAX:
                return Token('INT_CONST', int(token))
        elif token.startswith('"') and token.endswith('"'):
            return Token('STRING_CONST', token)
        else:
            return Token('IDENTIFIER', token)


@dataclass
class Token:
    token_type: str
    value: str | int


if __name__ == "__main__":
    jack_file_cleaner = JackTokenizer("../test/resources/SquareGame.jack")
    for line in jack_file_cleaner:
        print(line)
