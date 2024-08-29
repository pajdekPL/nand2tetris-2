from pathlib import Path
from xml.etree import ElementTree
from pytest import fixture
from jack_compiler.jack_compiler.compilation_engine import CompilationEngine
from jack_compiler.jack_compiler.jack_tokenizer import Token


def test_class_compilation_with_var_dev(tmp_path):
    expected_xml = """
    <class>
  <keyword> class </keyword>
  <identifier> SquareGame </identifier>
  <symbol> { </symbol>
  <classVarDec>
    <keyword> field </keyword>
    <identifier> Square </identifier>
    <identifier> square </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier> direction </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <symbol> } </symbol>
</class>"""
    xml_output_file_path = tmp_path / "test.xml"
    tokens = Generator([Token(token_type='KEYWORD', value='class'),
                        Token(token_type='IDENTIFIER', value='SquareGame'),
                        Token(token_type='SYMBOL', value='{'),
                        Token(token_type='KEYWORD', value='field'),
                        Token(token_type='IDENTIFIER', value='Square'),
                        Token(token_type='IDENTIFIER', value='square'),
                        Token(token_type='SYMBOL', value=';'),
                        Token(token_type='KEYWORD', value='field'),
                        Token(token_type='KEYWORD', value='int'),
                        Token(token_type='IDENTIFIER', value='direction'),
                        Token(token_type='SYMBOL', value=';'),
                        Token(token_type='SYMBOL', value='}'),
                        ])
    mocked_input_file = Path("")
    mocked_output_file = Path("")

    compilation_engine = CompilationEngine(mocked_input_file, mocked_output_file)
    compilation_engine.jack_tokens = tokens
    compilation_engine.compile_class()
    ElementTree.ElementTree(compilation_engine.xml_doc).write(xml_output_file_path, short_empty_elements=False)
    assert xml_output_file_path.read_text() == expected_xml

def test_compile_simple_class_header(tmp_path):
    xml_output_file_path = tmp_path / "test.xml"
    tokens = [Token(token_type='KEYWORD', value='class'),
              Token(token_type='IDENTIFIER', value='SudokuBoard'),
              Token(token_type='SYMBOL', value='{'),
              Token(token_type='KEYWORD', value='field'),
              Token(token_type='IDENTIFIER', value='Array'),
              Token(token_type='IDENTIFIER', value='allFields'),
                          Token(token_type='SYMBOL', value=','),
                          Token(token_type='IDENTIFIER', value='checkerArray'),
                          Token(token_type='SYMBOL', value=';'),
                          Token(token_type='KEYWORD', value='field'),
                          Token(token_type='KEYWORD', value='int'),
                          Token(token_type='IDENTIFIER', value='singleBlockRows'),
                          Token(token_type='SYMBOL', value=','),
                          Token(token_type='IDENTIFIER', value='singleBlockColumns'),
                          Token(token_type='SYMBOL', value=','),
                          Token(token_type='IDENTIFIER', value='totalRowsNum'),
                          Token(token_type='SYMBOL', value=';'),
                          Token(token_type='SYMBOL', value='}')
                          ]
    mocked_input_file = Path("")
    mocked_output_file = Path("")

    compilation_engine = CompilationEngine(mocked_input_file, mocked_output_file)
    compilation_engine.jack_tokens = Generator(tokens)
    compilation_engine.compile_class()
    ElementTree.ElementTree(compilation_engine.xml_doc).write(xml_output_file_path, short_empty_elements=False)
    assert xml_output_file_path.read_text() == ""

def test_let_statement_compilation(tmp_path, generator_jack_tokens_let_statement):
    xml_output_file_path = tmp_path/"test.xml"
    let_tokens = (token for token in [Token('KEYWORD', 'let'),
                  Token('IDENTIFIER', 'totalRowsNum'),
                  Token('SYMBOL', '='),
                  Token('INT_CONST', 3),
                  Token('SYMBOL', ';')])
    expected_xml = "<letStatement><keyword>let</keyword><identifier>totalRowsNum</identifier><symbol>=</symbol>" \
                   "<expression><term><integerConstant>3</integerConstant></expression></term></letStatement>"
    xml_doc = ElementTree.Element("letStatement")
    mocked_input_file = Path("")
    mocked_output_file = Path("")

    compilation_engine = CompilationEngine(mocked_input_file, mocked_output_file)
    compilation_engine.jack_tokens = generator_jack_tokens_let_statement
    compilation_engine.compile_let_statement(xml_doc)

    tree = ElementTree.ElementTree(xml_doc)
    tree.write(xml_output_file_path, short_empty_elements=False)
    assert xml_output_file_path.read_text() == expected_xml


class Generator:

    def __init__(self, tokens: list):
        self.items = tokens
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index >= len(self.items):
            raise StopIteration
        return self.items[self.index]

    def move_backward(self):
        if self.index > -1:
            self.index -= 1

@fixture
def generator_jack_tokens_let_statement():
    class Generator:
        def __init__(self):
            self.items = [Token('KEYWORD', 'let'),
                  Token('IDENTIFIER', 'totalRowsNum'),
                  Token('SYMBOL', '='),
                  Token('INT_CONST', 3),
                  Token('SYMBOL', ';')]
            self.index = -1

        def __iter__(self):
            return self

        def __next__(self):
            self.index += 1
            if self.index >= len(self.items):
                raise StopIteration
            return self.items[self.index]

        def move_backward(self):
            if self.index > -1:
                self.index -= 1
    return Generator()
