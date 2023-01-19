import re
from pathlib import Path
from dataclasses import dataclass


CMDS_MAPPING = {
    "add": "C_ARITHMETIC",
    "sub": "C_ARITHMETIC",
    "neg": "C_ARITHMETIC",
    "eq": "C_ARITHMETIC",
    "gt": "C_ARITHMETIC",
    "lt": "C_ARITHMETIC",
    "and": "C_ARITHMETIC",
    "or": "C_ARITHMETIC",
    "not": "C_ARITHMETIC",
    "push": "C_PUSH",
    "pop": "C_POP",
    "label": "C_LABEL",
    "goto": "C_GOTO",
    "if-goto": "C_IF",
    "function": "C_FUNCTION",
    "return": "C_RETURN",
    "call": "C_CALL",

}


@dataclass
class Command:
    cmd_type: str
    arg_1: str
    arg_2: int = None


class Parser:
    COMMENT_SIGN = "//"

    def __init__(self, input_file: Path):
        self.input_file = input_file
        self.parser_generator = self._generator()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.parser_generator)

    def _generator(self):
        with open(self.input_file) as file:
            for line in file:
                cmd_line = self._remove_comments_and_spaces_from_line_and_return(
                    line
                )
                if cmd_line:
                    yield self._parse_cmd(cmd_line)

    @staticmethod
    def has_more_commands():
        pass

    @staticmethod
    def _parse_cmd(line) -> Command:
        cmd = line.split()[0]
        c_cmd = CMDS_MAPPING.get(cmd)
        if c_cmd == "C_ARITHMETIC":
            return Parser._parse_arithmetic_command(line)
        if c_cmd == "C_PUSH":
            return Parser._parse_push_command(line)
        if c_cmd == "C_POP":
            return Parser._parse_pop_command(line)
        if c_cmd in {"C_LABEL", "C_GOTO", "C_IF"}:
            return Parser._parse_one_arg_command(line)
        if not c_cmd:
            raise UnknownCommand(f"{cmd} can't be parsed")

    @staticmethod
    def _parse_arithmetic_command(line) -> Command:
        return Command(CMDS_MAPPING[line], line)

    @staticmethod
    def _parse_push_command(line) -> Command:
        cmd_elements = line.split()
        return Command(
            CMDS_MAPPING[cmd_elements[0]], cmd_elements[1], int(cmd_elements[2])
        )

    @staticmethod
    def _parse_pop_command(line) -> Command:
        cmd_elements = line.split()
        return Command(
            CMDS_MAPPING[cmd_elements[0]], cmd_elements[1], int(cmd_elements[2])
        )

    @staticmethod
    def _remove_comments_and_spaces_from_line_and_return(line) -> str:
        if Parser.COMMENT_SIGN in line:
            return re.sub(
                r"\s{2,}", " ", line[: line.find(Parser.COMMENT_SIGN)].strip()
            )
        return re.sub(r"\s{2,}", " ", line.strip())

    @staticmethod
    def _parse_one_arg_command(line):
        cmd_elements = line.split()
        return Command(CMDS_MAPPING[cmd_elements[0]], cmd_elements[1])


class UnknownCommand(Exception):
    pass
