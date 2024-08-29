from pathlib import Path
from dataclasses import dataclass
from jack_compiler.jack_compiler.jack_tokenizer import JackTokenizer
from xml.etree import ElementTree


class CompilationEngine:
    XML_TAGS = {
        "IDENTIFIER": "identifier",
        "SYMBOL": "symbol",
        "INT_CONST": "integerConstant",
        "KEYWORD": "keyword",
        "STRING_CONST": "stringConstant"
    }
    CLASS_VAR_DEC_KEYWORDS = {
        "static",
        "field"
    }
    TYPE_KEYWORDS_VALUES = {
        'int',
        'char',
        'boolean',
    }
    CLASS_SUBROUTINE_DEV_KEYWORDS = {
        "constructor",
        "function",
        "method"
    }
    OP = {
        '+',
        '-',
        '*',
        '/',
        '&',
        '|',
        '<',
        '>',
        '=',
    }

    KEYWORD_CONSTANTS = {
        "this",
        "true",
        "false",
        "null",
    }

    def __init__(self, jack_file: Path, output_file: Path):
        self.jack_file = jack_file
        self.output_file = output_file
        self.open_file = None
        self.jack_tokens = None
        self.xml_output = []
        self.xml_doc = None

    def read_tokens(self):
        self.jack_tokens = JackTokenizer(self.jack_file)

    def _open_file_to_write_if_not_opened(self):
        return
        # if not self.open_file:
        #     self.open_file = open(self.jack_file, "w")

    def _get_next_token(self):
        return next(self.jack_tokens)

    def _move_token_backward(self):
        self.jack_tokens.move_backward()

    def compile_class_header(self):
        self.xml_doc = ElementTree.Element("class")
        token = self._get_next_token()
        if not(token.token_type == "KEYWORD" and token.value == "class"):
            raise CompilationError("Keyword 'class' expected")
        else:
            ElementTree.SubElement(self.xml_doc, CompilationEngine.XML_TAGS['KEYWORD']).text = "class"
        token = self._get_next_token()
        if not token.token_type == "IDENTIFIER":
            raise CompilationError("Identifier expected")
        else:
            ElementTree.SubElement(self.xml_doc, CompilationEngine.XML_TAGS["IDENTIFIER"]).text = token.value
        token = self._get_next_token()
        if not token.value == "{":
            raise CompilationError("'{' expected")
        else:
            ElementTree.SubElement(self.xml_doc, CompilationEngine.XML_TAGS["SYMBOL"]).text = token.value

    def compile_class(self):
        if not self.jack_tokens:
            raise CompilationError("Please initialize tokens, use: the 'read_tokens' method")
        self.compile_class_header()
        token = self._get_next_token()
        if token.token_type == "KEYWORD" and token.value in self.CLASS_VAR_DEC_KEYWORDS:
            self._move_token_backward()

            self.compile_class_var_dec()
            token = self._get_next_token()
        if token.token_type == "KEYWORD" and token.value in self.CLASS_SUBROUTINE_DEV_KEYWORDS:
            self._move_token_backward()
            subroutine_xml = ElementTree.SubElement(self.xml_doc, "subroutineDec")
            self.compile_subroutine(subroutine_xml)
        if not token.value == "}":
            raise CompilationError(f"'closing curly bracket' expected, get instead: {token}")
        else:
            ElementTree.SubElement(self.xml_doc, CompilationEngine.XML_TAGS["SYMBOL"]).text = token.value
        try:
            token = self._get_next_token()
        except StopIteration:
            return
        raise CompilationError(f"Not compiled token left: {token}")
        
    def compile_class_var_dec(self):
        token = self._get_next_token()
        class_var_dev_xml = ElementTree.SubElement(self.xml_doc, "classVarDec")
        ElementTree.SubElement(class_var_dev_xml, token.token_type.lower()).text = token.value
        # static, field
        token = next(self.jack_tokens)
        ElementTree.SubElement(class_var_dev_xml, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        # type int char boolean className
        token = next(self.jack_tokens)
        ElementTree.SubElement(class_var_dev_xml, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        # varName - identifier
        while token.value != ";":
            token = next(self.jack_tokens)
            ElementTree.SubElement(class_var_dev_xml, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        token = self._get_next_token()
        if token.value in CompilationEngine.CLASS_VAR_DEC_KEYWORDS:
            self.compile_class_var_dec()
        else:
            self.jack_tokens.move_backward()
            return
    def compile_subroutine(self, xml_parent):
        token = next(self.jack_tokens)
        ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        # return type
        token = next(self.jack_tokens)
        ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        # subroutine name
        token = next(self.jack_tokens)
        ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        token = next(self.jack_tokens)
        if token.value == "(":
            ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
            self.compile_parameter_list(xml_parent)
            token = next(self.jack_tokens)
            ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
            token = next(self.jack_tokens)
        if token.value == "{":
            ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
            subroutine_body = ElementTree.SubElement(xml_parent, "subroutineBody")
            self.compile_subroutine_body(subroutine_body)

    def compile_parameter_list(self, parent):
        # parameterList
        token = next(self.jack_tokens)
        current_parent = ElementTree.SubElement(parent, "parameterList")
        # ElementTree.SubElement(current_parent, "s").text = "s"
        while token.value != ")":
            if (token.token_type == "KEYWORD" and token.value in CompilationEngine.TYPE_KEYWORDS_VALUES) or token.token_type == "IDENTIFIER":
                ElementTree.SubElement(current_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
            token = next(self.jack_tokens)
        self.jack_tokens.move_backward()

    def compile_subroutine_body(self, parent):
        # subroutineBody
        token = next(self.jack_tokens)
        if token.value == "var":
            var_dec_xml = ElementTree.SubElement(parent, "varDec")
            self.jack_tokens.move_backward()
            self.compile_var_dec(var_dec_xml)
        token = next(self.jack_tokens)
        statements_xml = ElementTree.SubElement(parent, "statements")
        if token.value != "}":
            self.jack_tokens.move_backward()
            self.compile_statements(statements_xml)

    def compile_var_dec(self, xml_parent):
        token = next(self.jack_tokens)
        ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        while token.value != ";":
            token = next(self.jack_tokens)
            ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        token = next(self.jack_tokens)
        if token.value != "var":
            self.jack_tokens.move_backward()
            return
        self.compile_var_dec(xml_parent)

    def compile_statements(self, xml_parent):
        token = next(self.jack_tokens)
        if token.value == "let":
            let_xml = ElementTree.SubElement(xml_parent, "letStatement")
            self.jack_tokens.move_backward()
            self.compile_let_statement(let_xml)

    def compile_let_statement(self, xml_parent):
        token = next(self.jack_tokens)
        ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        token = next(self.jack_tokens)
        ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
        token = next(self.jack_tokens)
        if token.value == "=":
            ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
            expression_xml = ElementTree.SubElement(xml_parent, "expression")
            self.compile_expression(expression_xml)
        ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value
    def compile_if_statement(self):
        pass

    def compile_while_statement(self):
        pass

    def compile_do(self):
        pass

    def compile_return(self):
        pass

    def compile_expression(self, xml_parent):
        token = next(self.jack_tokens)
        if token.value == ";":
            self.jack_tokens.move_backward()
            return
        if token.value not in CompilationEngine.OP:
            term_xml = ElementTree.SubElement(xml_parent, "term")
            self.jack_tokens.move_backward()
            self.compile_term(term_xml)
        else:
            ElementTree.SubElement(xml_parent, CompilationEngine.XML_TAGS[token.token_type]).text = token.value

    def compile_term(self, xml_parent):
        token = next(self.jack_tokens)
        if token.value == ";":
            self.jack_tokens.move_backward()
            return
        if token.token_type == "KEYWORD" and token.value in CompilationEngine.KEYWORD_CONSTANTS:
            pass

    def compile_expression_list(self):
        pass


class CompilationError(Exception):
    pass


if __name__ == "__main__":
    comp_engine = CompilationEngine("../test/resources/SimpleClassFieldsDec.jack", "twojstary.xml")
    comp_engine.read_tokens()
    comp_engine.compile_class()
    tree = ElementTree.ElementTree(comp_engine.xml_doc)
    tree.write("test.xml", short_empty_elements=False)
    print(comp_engine.xml_output)
    from xml.dom.minidom import parseString
    with open("test.xml") as file:
        print(parseString(file.read()).toprettyxml())
