from pathlib import Path
from datetime import datetime
from vm_translator.parser import Command


class CodeWriter:
    def __init__(self, file_path: Path):
        self.label_counter = {
            "gt": 0,
            "lt": 0,
            "eq": 0,
        }
        self.file_path = file_path
        self.open_file = None
        self.module_name = file_path.name[: file_path.name.find(".")]
        self._write_header_to_file()
        self._c_arithmetic_cmd_mapping = {
            "add": self._generate_add_cmd,
            "sub": self._generate_sub_cmd,
            "gt": self._generate_gt_cmd,
            "lt": self._generate_lt_cmd,
            "eq": self._generate_eq_cmd,
            "not": self._generate_not_cmd,
            "or": self._generate_or_cmd,
            "and": self._generate_and_cmd,
            "neg": self._generate_neg_cmd,
        }
        self._c_push_cmd_mapping = {
            "constant": self._generate_push_constant_cmd,
            "argument": self._generate_push_cmd_for_local_argument_this_that,
            "local": self._generate_push_cmd_for_local_argument_this_that,
            "this": self._generate_push_cmd_for_local_argument_this_that,
            "that": self._generate_push_cmd_for_local_argument_this_that,
            "temp": self._generate_push_temp_cmd,
            "static": self._generate_push_static_cmd,
            "pointer": self._generate_push_pointer_cmd,
        }
        self._c_pop_cmd_mapping = {
            "argument": self._generate_pop_cmd_for_local_argument_this_that,
            "local": self._generate_pop_cmd_for_local_argument_this_that,
            "this": self._generate_pop_cmd_for_local_argument_this_that,
            "that": self._generate_pop_cmd_for_local_argument_this_that,
            "temp": self._generate_pop_temp_cmd,
            "static": self._generate_pop_static_cmd,
            "pointer": self._generate_pop_pointer_cmd,
        }

    def write_cmd(self, cmd: Command):
        self._open_file_to_write_if_not_opened()
        if cmd.cmd_type == "C_ARITHMETIC":
            self.open_file.writelines(self._generate_c_arithmetic_cmd(cmd))
        elif cmd.cmd_type == "C_PUSH":
            self.open_file.writelines(self._generate_c_push_cmd(cmd))
        elif cmd.cmd_type == "C_POP":
            self.open_file.writelines(self._generate_c_pop_cmd(cmd))
        else:
            self._raise_unrecognised_cmd(cmd)

    def _write_header_to_file(self):
        self._open_file_to_write_if_not_opened()
        self.open_file.writelines(
            f"// ASM FILE created by VMTranslator created by pajdek.\n"
            f"// Compilation date: {datetime.today()}"
        )

    def _generate_c_arithmetic_cmd(self, cmd):
        c_arithmetic_function = self._c_arithmetic_cmd_mapping.get(cmd.arg_1)
        if not c_arithmetic_function:
            self._raise_unrecognised_cmd(cmd)
        return c_arithmetic_function()

    def _generate_c_push_cmd(self, cmd):
        c_push_function = self._c_push_cmd_mapping.get(cmd.arg_1)
        if not c_push_function:
            self._raise_unrecognised_cmd(cmd)
        return c_push_function(cmd)

    def _generate_c_pop_cmd(self, cmd):
        c_pop_function = self._c_pop_cmd_mapping.get(cmd.arg_1)
        if not c_pop_function:
            self._raise_unrecognised_cmd(cmd)
        return c_pop_function(cmd)

    @staticmethod
    def _raise_unrecognised_cmd(cmd):
        raise UnrecognisedCmdError(
            f"{cmd} is not handled by the compiler, check your VM code"
        )

    def _open_file_to_write_if_not_opened(self):
        if not self.open_file:
            self.open_file = open(self.file_path, "w")

    def close_file(self):
        self.open_file.close()

    @staticmethod
    def _generate_add_cmd():
        command_lines = ("\n// add", "@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M")
        return "\n".join(command_lines)

    @staticmethod
    def _generate_sub_cmd():
        command_lines = ("\n// sub", "@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D")
        return "\n".join(command_lines)

    @staticmethod
    def _generate_or_cmd():
        command_lines = ("\n// or", "@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M")
        return "\n".join(command_lines)

    @staticmethod
    def _generate_and_cmd():
        command_lines = ("\n// and", "@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M")
        return "\n".join(command_lines)

    @staticmethod
    def _generate_not_cmd():
        command_lines = ("\n// or", "@SP", "A=M-1", "M=!M")
        return "\n".join(command_lines)

    @staticmethod
    def _generate_neg_cmd():
        command_lines = ("\n// or", "@SP", "A=M-1", "M=-M")
        return "\n".join(command_lines)

    def _generate_gt_cmd(self):
        label = self.label_counter["gt"]
        self.label_counter["gt"] = label + 1
        command_lines = (
            "\n// gt",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "M=D",
            "@SP",
            "A=M-1",
            "D=M",
            "@R13",
            "D=D-M",
            f"@gt{label}",
            "D; JGT",
            "@SP",
            "A=M-1",
            "M=0",
            f"@gtEND{label}",
            "0; JMP",
            f"(gt{label})",
            "@SP",
            "A=M-1",
            "M=-1",
            f"(gtEND{label})",
        )
        return "\n".join(command_lines)

    def _generate_lt_cmd(self):
        label = self.label_counter["lt"]
        self.label_counter["lt"] = label + 1
        command_lines = (
            "\n// gt",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "M=D",
            "@SP",
            "A=M-1",
            "D=M",
            "@R13",
            "D=D-M",
            f"@lt{label}",
            "D; JLT",
            "@SP",
            "A=M-1",
            "M=0",
            f"@ltEND{label}",
            "0; JMP",
            f"(lt{label})",
            "@SP",
            "A=M-1",
            "M=-1",
            f"(ltEND{label})",
        )
        return "\n".join(command_lines)

    def _generate_eq_cmd(self):
        label = self.label_counter["eq"]
        self.label_counter["eq"] = label + 1
        command_lines = (
            "\n// gt",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "M=D",
            "@SP",
            "A=M-1",
            "D=M",
            "@R13",
            "D=D-M",
            f"@eq{label}",
            "D; JEQ",
            "@SP",
            "A=M-1",
            "M=0",
            f"@eqEND{label}",
            "0; JMP",
            f"(eq{label})",
            "@SP",
            "A=M-1",
            "M=-1",
            f"(eqEND{label})",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_push_constant_cmd(cmd):
        command_lines = (
            f"\n//{cmd}",
            f"@{cmd.arg_2}",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_pop_local_cmd(cmd):
        command_lines = (
            f"\n//{cmd}",
            f"@{cmd.arg_2}",
            "D=A",
            "@LCL",
            "D=M+D",
            "@R13",
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "A=M",
            "M=D",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_push_cmd_for_local_argument_this_that(cmd):
        pointer_mapping = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }
        command_lines = (
            f"\n//{cmd}",
            f"@{cmd.arg_2}",
            "D=A",
            f"@{pointer_mapping[cmd.arg_1]}",
            "A=M+D",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_pop_cmd_for_local_argument_this_that(cmd):
        pointer_mapping = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }
        command_lines = (
            f"\n//{cmd}",
            f"@{cmd.arg_2}",
            "D=A",
            f"@{pointer_mapping[cmd.arg_1]}",
            "D=M+D",
            "@R13",
            "M=D",
            "@SP",
            "AM=M-1",
            "D=M",
            "@R13",
            "A=M",
            "M=D",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_push_temp_cmd(cmd):
        temp_start = 5
        command_lines = (
            f"\n//{cmd}",
            f"@{temp_start + cmd.arg_2}",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_pop_temp_cmd(cmd):
        temp_start = 5
        command_lines = (
            f"\n//{cmd}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{temp_start + cmd.arg_2}",
            "M=D",
        )
        return "\n".join(command_lines)

    def _generate_push_static_cmd(self, cmd):
        command_lines = (
            f"\n//{cmd}",
            f"@{self.file_name}.{cmd.arg_2}",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        )
        return "\n".join(command_lines)

    def _generate_pop_static_cmd(self, cmd):
        command_lines = (
            f"\n//{cmd}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{self.file_name}.{cmd.arg_2}",
            "M=D",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_push_pointer_cmd(cmd):
        pointer_mapping = {
            0: "THIS",
            1: "THAT",
        }
        command_lines = (
            f"\n//{cmd}",
            f"@{pointer_mapping[cmd.arg_2]}",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_pop_pointer_cmd(cmd):
        pointer_mapping = {
            0: "THIS",
            1: "THAT",
        }
        command_lines = (
            f"\n//{cmd}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{pointer_mapping[cmd.arg_2]}",
            "M=D",
        )
        return "\n".join(command_lines)


class UnrecognisedCmdError(Exception):
    pass
