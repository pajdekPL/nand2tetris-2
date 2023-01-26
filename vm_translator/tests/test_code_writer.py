from pathlib import Path
from unittest.mock import patch

import pytest

from vm_translator.parser import Command
from vm_translator.code_writer import CodeWriter, UnrecognisedCmdError


def test_code_writer_init(mockdata_time):
    mockdata_time.today.return_value = "2023-01-17 15:01:16"
    expected_label_counter = {
        "gt": 0,
        "lt": 0,
        "eq": 0,
    }
    expected_module_name = "mocked"
    mock_file = Path("tmp_path/mocked.asm")

    with patch("builtins.open") as mocked_open:
        code_writer = CodeWriter(mock_file)

        assert code_writer.file_name == expected_module_name
        assert code_writer.label_counter == expected_label_counter
        mocked_open.assert_not_called()


def test_code_writer_with_wrong_cmd_raises_proper_exception():
    mock_file = Path("tmp_path/mocked.asm")
    mocked_wrong_cmd = Command("C_DUMMY", "dummy", 10)

    with patch("builtins.open"):
        code_writer = CodeWriter(mock_file)
        with pytest.raises(UnrecognisedCmdError):
            code_writer.write_cmd(mocked_wrong_cmd)


@pytest.mark.parametrize(
    "command, asm_expected_code",
    [
        (Command("C_ARITHMETIC", "add"), "\n// add\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M"),
        (Command("C_ARITHMETIC", "sub"), "\n// sub\n@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D"),
        (
            Command("C_ARITHMETIC", "gt"),
            "\n// gt\n@SP\nAM=M-1\nD=M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nD=D-M\n@gt0\nD; "
            "JGT\n@SP\nA=M-1\nM=0\n@gtEND0\n0; JMP\n(gt0)\n@SP\nA=M-1\nM=-1\n(gtEND0)",
        ),
        (
            Command("C_ARITHMETIC", "lt"),
            "\n// gt\n@SP\nAM=M-1\nD=M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nD=D-M\n@lt0\nD; "
            "JLT\n@SP\nA=M-1\nM=0\n@ltEND0\n0; JMP\n(lt0)\n@SP\nA=M-1\nM=-1\n(ltEND0)",
        ),
        (
            Command("C_ARITHMETIC", "eq"),
            "\n// gt\n@SP\nAM=M-1\nD=M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nD=D-M\n@eq0\nD; "
            "JEQ\n@SP\nA=M-1\nM=0\n@eqEND0\n0; JMP\n(eq0)\n@SP\nA=M-1\nM=-1\n(eqEND0)",
        ),
        (Command("C_ARITHMETIC", "neg"), "\n// or\n@SP\nA=M-1\nM=-M"),
        (Command("C_ARITHMETIC", "or"), "\n// or\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M"),
        (Command("C_ARITHMETIC", "not"), "\n// or\n@SP\nA=M-1\nM=!M"),
        (Command("C_ARITHMETIC", "and"), "\n// and\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M"),
    ],
)
def test_code_writer_writes_arithmetic_commands_properly(command, asm_expected_code):
    mock_file = Path("tmp_path/mocked.asm")

    with patch("builtins.open") as mocked_open:
        code_writer = CodeWriter(mock_file)
        code_writer.write_cmd(command)

        mocked_open().writelines.assert_called_with(asm_expected_code)


@pytest.mark.parametrize(
    "command, asm_expected_code",
    [
        (
            Command("C_PUSH", "local", 2),
            "\n// Command(cmd_type='C_PUSH', arg_1='local', arg_2=2)"
            "\n@2\nD=A\n@LCL\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1",
        ),
        (
            Command("C_PUSH", "argument", 22),
            "\n// Command(cmd_type='C_PUSH', arg_1='argument', arg_2=22)"
            "\n@22\nD=A\n@ARG\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1",
        ),
        (
            Command("C_PUSH", "constant", 55),
            "\n// Command(cmd_type='C_PUSH', arg_1='constant', arg_2=55)"
            "\n@55\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1",
        ),
        (
            Command("C_PUSH", "pointer", 0),
            "\n// Command(cmd_type='C_PUSH', arg_1='pointer', "
            "arg_2=0)\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1",
        ),
        (
            Command("C_PUSH", "pointer", 1),
            "\n// Command(cmd_type='C_PUSH', arg_1='pointer', "
            "arg_2=1)\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1",
        ),
        (
            Command("C_PUSH", "temp", 5),
            "\n// Command(cmd_type='C_PUSH', arg_1='temp', arg_2=5)"
            "\n@10\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1",
        ),
        (
            Command("C_PUSH", "this", 5),
            "\n// Command(cmd_type='C_PUSH', arg_1='this', arg_2=5)"
            "\n@5\nD=A\n@THIS\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1",
        ),
    ],
)
def test_code_writer_writes_push_commands_properly(command, asm_expected_code):
    mock_file = Path("tmp_path/mocked.asm")
    with patch("builtins.open") as mocked_open:
        code_writer = CodeWriter(mock_file)
        code_writer.write_cmd(command)

        mocked_open().writelines.assert_called_with(asm_expected_code)


@pytest.mark.parametrize(
    "command, asm_expected_code",
    [
        (
            Command("C_POP", "local", 2),
            "\n// Command(cmd_type='C_POP', arg_1='local', arg_2=2)"
            "\n@2\nD=A\n@LCL\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D",
        ),
        (
            Command("C_POP", "argument", 22),
            "\n// Command(cmd_type='C_POP', arg_1='argument', arg_2=22)"
            "\n@22\nD=A\n@ARG\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D",
        ),
    ],
)
def test_code_writer_writes_pop_commands_properly(command, asm_expected_code):
    mock_file = Path("tmp_path/mocked.asm")
    with patch("builtins.open") as mocked_open:
        code_writer = CodeWriter(mock_file)
        code_writer.write_cmd(command)

        mocked_open().writelines.assert_called_with(asm_expected_code)


@pytest.mark.parametrize(
    "command, asm_expected_code",
    [
        (
            Command("C_LABEL", "loop"),
            "\n// Command(cmd_type='C_LABEL', arg_1='loop', arg_2=None)\n(loop)",
        ),
        (
            Command("C_IF", "loopDoop"),
            "\n// Command(cmd_type='C_IF', arg_1='loopDoop', arg_2=None)\n@SP\nAM=M-1\nD=M\n@loopDoop\nD;JNE",
        ),
        (
            Command("C_GOTO", "loopX"),
            "\n// Command(cmd_type='C_GOTO', arg_1='loopX', arg_2=None)\n@loopX\n0;JMP",
        ),
    ],
)
def test_code_writer_writes_branching_commands_properly(command, asm_expected_code):
    mock_file = Path("tmp_path/mocked.asm")
    with patch("builtins.open") as mocked_open:
        code_writer = CodeWriter(mock_file)
        code_writer.write_cmd(command)

        mocked_open().writelines.assert_called_with(asm_expected_code)


def test_label_indexes_are_incremented_properly_for_gt_cmd():
    mock_file = Path("tmp_path/mocked.asm")
    expected_label_counter_init = {
        "gt": 0,
        "lt": 0,
        "eq": 0,
    }
    expected_label_counter_after_two_gt_cmds = {
        "gt": 2,
        "lt": 0,
        "eq": 0,
    }
    command_1 = Command("C_ARITHMETIC", "gt")
    command_2 = Command("C_ARITHMETIC", "gt")
    with patch("builtins.open"):
        code_writer = CodeWriter(mock_file)

        assert code_writer.label_counter == expected_label_counter_init

        code_writer.write_cmd(command_1)
        code_writer.write_cmd(command_2)

    assert code_writer.label_counter == expected_label_counter_after_two_gt_cmds


@pytest.fixture
def mockdata_time():
    with patch("vm_translator.code_writer.datetime") as mocked_datatime:
        yield mocked_datatime
