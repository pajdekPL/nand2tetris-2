import os
from unittest import mock
from pathlib import Path
import pytest
from vm_translator.parser import Parser, Command

resource_dir = Path(os.path.dirname(__file__)) / "resources/"


def test_parser_with_simple_add():
    simple_add_file_path = resource_dir / "SimpleAdd.vm"

    parser = Parser(simple_add_file_path)
    cmd = next(parser)

    assert cmd.cmd_type == "C_PUSH"
    assert cmd.arg_1 == "constant"
    assert cmd.arg_2 == 7


@pytest.mark.parametrize(
    "cmd_line, expected_parsed_line",
    [
        ("push constant 2", "push constant 2"),
        ("// it is a comment ", ""),
        ("pop local 5   // pop local 5", "pop local 5"),
        ("     ", ""),
        ("  \n    ", ""),
    ],
)
def test_remove_comments_and_spaces_from_line_and_return(
    cmd_line, expected_parsed_line
):
    assert (
        Parser._remove_comments_and_spaces_from_line_and_return(cmd_line)
        == expected_parsed_line
    )


@pytest.mark.parametrize(
    "input_line, expected_cmd",
    [
        ("\nadd //some_comment", Command("C_ARITHMETIC", "add")),
        ("\nsub\n", Command("C_ARITHMETIC", "sub")),
        ("\nneg\n", Command("C_ARITHMETIC", "neg")),
        ("\neq\n", Command("C_ARITHMETIC", "eq")),
        ("\ngt\n", Command("C_ARITHMETIC", "gt")),
        ("\nlt\n", Command("C_ARITHMETIC", "lt")),
        ("\nand\n", Command("C_ARITHMETIC", "and")),
        ("\nor", Command("C_ARITHMETIC", "or")),
        ("\nnot", Command("C_ARITHMETIC", "not")),
    ],
)
def test_parser_with_arithmetic_cmds(input_line, expected_cmd):
    with mock.patch("builtins.open", mock.mock_open(read_data=input_line)):
        parser = Parser(Path("mock/file"))
        cmd = next(parser)

        assert cmd.cmd_type == expected_cmd.cmd_type
        assert cmd.arg_1 == expected_cmd.arg_1
        assert cmd.arg_2 is None


@pytest.mark.parametrize(
    "input_line, expected_cmd",
    [
        ("\npush constant 3\n", Command("C_PUSH", "constant", 3)),
        ("\npush local 5 // some comment", Command("C_PUSH", "local", 5)),
    ],
)
def test_parser_with_push_cmds(input_line, expected_cmd):
    with mock.patch("builtins.open", mock.mock_open(read_data=input_line)):
        parser = Parser(Path("mock/file"))
        cmd = next(parser)

        assert cmd.cmd_type == expected_cmd.cmd_type
        assert cmd.arg_1 == expected_cmd.arg_1
        assert cmd.arg_2 == expected_cmd.arg_2


@pytest.mark.parametrize(
    "input_line, expected_cmd",
    [
        ("\npush constant 3\n", Command("C_PUSH", "constant", 3)),
        ("\npush local 5 // some comment", Command("C_PUSH", "local", 5)),
    ],
)
def test_parser_with_push_cmds_context_manager(input_line, expected_cmd):
    with mock.patch("builtins.open", mock.mock_open(read_data=input_line)):
        with Parser(Path("mock/file")) as parser:
            cmd = next(parser)
            assert cmd.cmd_type == expected_cmd.cmd_type
            assert cmd.arg_1 == expected_cmd.arg_1
            assert cmd.arg_2 == expected_cmd.arg_2


@pytest.mark.parametrize(
    "input_line, expected_cmd",
    [
        ("\npop constant 3\n", Command("C_POP", "constant", 3)),
        ("\npop local 5 // some comment", Command("C_POP", "local", 5)),
    ],
)
def test_parser_with_pop_cmds_context_manager(input_line, expected_cmd):
    with mock.patch("builtins.open", mock.mock_open(read_data=input_line)):
        with Parser(Path("mock/file")) as parser:
            cmd = next(parser)
            assert cmd.cmd_type == expected_cmd.cmd_type
            assert cmd.arg_1 == expected_cmd.arg_1
            assert cmd.arg_2 == expected_cmd.arg_2


def test_parser_usage_as_iterator():
    expected_cmds = (
        Command("C_ARITHMETIC", "add"),
        Command("C_ARITHMETIC", "sub"),
        Command("C_POP", "constant", 3),
    )
    read_data = "add\nsub\npop constant  3"

    with mock.patch("builtins.open", mock.mock_open(read_data=read_data)):
        with Parser(Path("mock/file")) as parser:
            for i, cmd in enumerate(parser):

                assert cmd.cmd_type == expected_cmds[i].cmd_type
                assert cmd.arg_1 == expected_cmds[i].arg_1
                assert cmd.arg_2 == expected_cmds[i].arg_2

            with pytest.raises(StopIteration):
                next(parser)


@pytest.mark.parametrize("vm_cmd, expected_parsed_cmd", [
    ("label loop", Command("C_LABEL", "loop")),
    ("goto someLoop", Command("C_GOTO", "someLoop")),
    ("if-goto loop", Command("C_IF", "loop")),
])
def test_parser_with_branching_cmds(vm_cmd, expected_parsed_cmd):
    with mock.patch("builtins.open", mock.mock_open(read_data=vm_cmd)):
        parser = Parser(Path("mock/file"))
        cmd = next(parser)
        assert cmd.cmd_type == expected_parsed_cmd.cmd_type
        assert cmd.arg_1 == expected_parsed_cmd.arg_1
        assert cmd.arg_2 is None
