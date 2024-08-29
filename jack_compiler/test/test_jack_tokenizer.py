from pathlib import Path
from unittest.mock import patch
import pytest
import os
from jack_compiler.jack_compiler.jack_tokenizer import JackFileCleaner, JackTokenizer, Token


resource_dir = Path(os.path.dirname(__file__)) / "resources/"


@pytest.mark.parametrize("jack_file_content, expected_result", [
    ('constructor SudokuBoard new() {\nlet totalRowsNum = 3;\n}', [Token("KEYWORD", "constructor"),
                                                                   Token("IDENTIFIER", "SudokuBoard"),
                                                                   Token("IDENTIFIER", "new"),
                                                                   Token("SYMBOL", "("),
                                                                   Token("SYMBOL", ")"),
                                                                   Token("SYMBOL", "{"),
                                                                   Token('KEYWORD', 'let'),
                                                                   Token('IDENTIFIER', 'totalRowsNum'),
                                                                   Token('SYMBOL', '='),
                                                                   Token('INT_CONST', 3),
                                                                   Token('SYMBOL', ';'),
                                                                   Token('SYMBOL', '}'),
                                                                   ])
])
def test_jack_tokenizer(tmp_path, jack_file_content, expected_result):
    temp_jack_file = tmp_path/"temp.jack"
    temp_jack_file.write_text(jack_file_content)
    jack_tokenizer = JackTokenizer(temp_jack_file)
    assert list(jack_tokenizer) == expected_result


def test_jack_file_cleaner_removes_all_comments_and_whitespaces_properly():
    expected_code_lines_list = ['class Main {',
                                'function void main() {',
                                'var Array a;',
                                'var int dummy_int;',
                                'var int length;',
                                'var int i, sum;',
                                'let length = Keyboard.readInt("HOW MANY NUMBERS? ");',
                                'let a = Array.new(length);',
                                'let i = 0;',
                                'while (i < length) {',
                                'let a[i] = Keyboard.readInt("ENTER THE NEXT NUMBER: ");',
                                'let i = i + 1;',
                                '}',
                                'let i = 0;',
                                'let sum = 0;',
                                '}',
                                '}'
                              ]
    jack_file_with_comments = resource_dir / "JackProgramWithComments.jack"

    jack_file_cleaner = JackFileCleaner(jack_file_with_comments)

    assert jack_file_cleaner.clean_file_from_comments_and_white_spaces_and_return_code_lines() == \
           expected_code_lines_list

