from pathlib import Path
from datetime import datetime
from vm_translator.parser import Command


class CodeWriter:
    def __init__(self, file_path: Path, write_header=False):
        self.label_counter = {
            "gt": 0,
            "lt": 0,
            "eq": 0,
        }
        self.file_path = file_path
        self.open_file = None
        self.file_name = file_path.name[: file_path.name.find(".")]
        self._current_return_labels = {}
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
        if write_header:
            self._write_header_to_file()

    def write_cmd(self, cmd: Command):
        self._open_file_to_write_if_not_opened()
        if cmd.cmd_type == "C_ARITHMETIC":
            self.open_file.writelines(self._generate_c_arithmetic_cmd(cmd))
        elif cmd.cmd_type == "C_PUSH":
            self.open_file.writelines(self._generate_c_push_cmd(cmd))
        elif cmd.cmd_type == "C_POP":
            self.open_file.writelines(self._generate_c_pop_cmd(cmd))
        elif cmd.cmd_type == "C_LABEL":
            self.open_file.writelines(self._generate_c_label_cmd(cmd))
        elif cmd.cmd_type == "C_GOTO":
            self.open_file.writelines(self._generate_c_goto_cmd(cmd))
        elif cmd.cmd_type == "C_IF":
            self.open_file.writelines(self._generate_c_if_cmd(cmd))
        elif cmd.cmd_type == "C_FUNCTION":
            self.open_file.writelines(self._generate_c_function_cmd(cmd))
        elif cmd.cmd_type == "C_RETURN":
            self.open_file.writelines(self._generate_c_return_cmd(cmd))
        elif cmd.cmd_type == "C_CALL":
            self.open_file.writelines(self._generate_c_call_cmd(cmd))
        else:
            self._raise_unrecognised_cmd(cmd)

    def _write_header_to_file(self):
        """
        SP = 256
        call Sys.init
        :return:
        """

        self._open_file_to_write_if_not_opened()
        self.open_file.writelines(
            f"// ASM FILE created by VMTranslator created by pajdek.\n"
            f"// Compilation date: {datetime.today()}\n"
        )
        self.open_file.writelines("// set SP to 256\n" "@256\n" "D=A\n" "@SP\n" "M=D\n")
        self.write_cmd(Command("C_CALL", "Sys.init", 0))

    def _generate_c_arithmetic_cmd(self, cmd: Command):
        c_arithmetic_function = self._c_arithmetic_cmd_mapping.get(cmd.arg_1)
        if not c_arithmetic_function:
            self._raise_unrecognised_cmd(cmd)
        return c_arithmetic_function()

    def _generate_c_push_cmd(self, cmd: Command):
        c_push_function = self._c_push_cmd_mapping.get(cmd.arg_1)
        if not c_push_function:
            self._raise_unrecognised_cmd(cmd)
        return c_push_function(cmd)

    def _generate_c_pop_cmd(self, cmd: Command):
        c_pop_function = self._c_pop_cmd_mapping.get(cmd.arg_1)
        if not c_pop_function:
            self._raise_unrecognised_cmd(cmd)
        return c_pop_function(cmd)

    @staticmethod
    def _raise_unrecognised_cmd(cmd: Command):
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
    def _generate_push_constant_cmd(cmd: Command):
        command_lines = (
            f"\n// {cmd}",
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
    def _generate_pop_local_cmd(cmd: Command):
        command_lines = (
            f"\n// {cmd}",
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
    def _generate_push_cmd_for_local_argument_this_that(cmd: Command):
        pointer_mapping = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }
        command_lines = (
            f"\n// {cmd}",
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
    def _generate_pop_cmd_for_local_argument_this_that(cmd: Command):
        pointer_mapping = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }
        command_lines = (
            f"\n// {cmd}",
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
    def _generate_push_temp_cmd(cmd: Command):
        temp_start = 5
        command_lines = (
            f"\n// {cmd}",
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
    def _generate_pop_temp_cmd(cmd: Command):
        temp_start = 5
        command_lines = (
            f"\n// {cmd}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{temp_start + cmd.arg_2}",
            "M=D",
        )
        return "\n".join(command_lines)

    def _generate_push_static_cmd(self, cmd: Command):
        command_lines = (
            f"\n// {cmd}",
            f"@{self.file_name}.{cmd.arg_2}",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
        )
        return "\n".join(command_lines)

    def _generate_pop_static_cmd(self, cmd: Command):
        command_lines = (
            f"\n// {cmd}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{self.file_name}.{cmd.arg_2}",
            "M=D",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_push_pointer_cmd(cmd: Command):
        pointer_mapping = {
            0: "THIS",
            1: "THAT",
        }
        command_lines = (
            f"\n// {cmd}",
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
    def _generate_pop_pointer_cmd(cmd: Command):
        pointer_mapping = {
            0: "THIS",
            1: "THAT",
        }
        command_lines = (
            f"\n// {cmd}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{pointer_mapping[cmd.arg_2]}",
            "M=D",
        )
        return "\n".join(command_lines)

    @staticmethod
    def _generate_c_label_cmd(cmd: Command):
        command_lines = [f"\n// {cmd}", f"({cmd.arg_1})"]
        return "\n".join(command_lines)

    @staticmethod
    def _generate_c_goto_cmd(cmd: Command):
        command_lines = [f"\n// {cmd}", f"@{cmd.arg_1}", "0;JMP"]
        return "\n".join(command_lines)

    @staticmethod
    def _generate_c_if_cmd(cmd: Command):
        command_lines = [
            f"\n// {cmd}",
            "@SP",
            "AM=M-1",
            "D=M",
            f"@{cmd.arg_1}",
            "D;JNE",
        ]
        return "\n".join(command_lines)

    @staticmethod
    def _generate_c_function_cmd(cmd: Command):
        set_local_vars = ""
        push_0 = "@SP\nA=M\nM=0\n@SP\nM=M+1\n"
        if cmd.arg_2:
            set_local_vars = cmd.arg_2 * push_0
        command_lines = [
            f"\n// {cmd}",
            f"({cmd.arg_1})",
            set_local_vars,
        ]
        return "\n".join(command_lines)

    def _generate_c_call_cmd(self, cmd: Command):
        """
        PUSH returnAddress
        PUSH LCL
        PUSH ARG
        PUSH THIS
        PUSH THAT
        ARG = SP - 5 - nArgs
        LCL = SP
        goto functionName
        (returnAddress)
        :param cmd:
        :return:
        """
        func_return_label = self._generate_func_return_label()
        command_lines = [
            f"\n// {cmd}",
            # PUSH returnAddress
            f"@{func_return_label}",
            "D=A",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            # PUSH LCL
            "@LCL",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            # PUSH ARG
            "@ARG",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            # PUSH THIS
            "@THIS",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            # PUSH THAT
            "@THAT",
            "D=M",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1",
            # ARG = SP - 5 - nArgs
            "@5",
            "D=A",
            "@R14",
            "M=D",
            f"@{cmd.arg_2}",
            "D=A",
            "@R14",
            "M=M+D",
            "@SP",
            "D=M",
            "@R14",
            "MD=D-M",
            "@ARG",
            "M=D",
            # LCL = SP
            "@SP",
            "D=M",
            "@LCL",
            "M=D",
            # goto
            f"@{cmd.arg_1}",
            "0;JMP",
            f"({func_return_label})",
        ]
        return "\n".join(command_lines)

    def _generate_func_return_label(self):
        template = "{file_name}$ret.{count}"

        if not self._current_return_labels.get(self.file_name):
            self._current_return_labels[self.file_name] = 1
            return template.format(file_name=self.file_name, count=1)
        self._current_return_labels[self.file_name] += 1
        return template.format(
            file_name=self.file_name, count=self._current_return_labels[self.file_name]
        )

    @staticmethod
    def _generate_c_return_cmd(cmd: Command):
        """
        endFrame = LCL
        retAddr = *(endFrame - 5)
        *ARG = POP()

        :param cmd:
        :return:
        """
        command_lines = [
            f"\n// {cmd}",
            # endFrame = LCL
            "@LCL",
            "D=M",
            "@endFrame",
            "M=D",
            # retAddr = *(endFrame - 5)
            "@5",
            "D=A",
            "@endFrame",
            "A=M-D",
            "D=M",
            "@retAddr",
            "M=D",
            # *ARG = POP()
            "@SP",
            "AM=M-1",
            "D=M",
            "@ARG",
            "A=M",
            "M=D",
            # SP = ARG + 1
            "@ARG",
            "D=M",
            "@SP",
            "M=D+1",
            # THAT = *(endFrame - 1)
            "@endFrame",
            "A=M-1",
            "D=M",
            "@THAT",
            "M=D",
            # THIS = *(endFrame - 2)
            "@endFrame",
            "A=M-1",
            "A=A-1",
            "D=M",
            "@THIS",
            "M=D",
            # ARG = *(endFrame - 3)
            "@endFrame",
            "A=M-1",
            "A=A-1",
            "A=A-1",
            "D=M",
            "@ARG",
            "M=D",
            # LCL = *(endFrame - 4)
            "@endFrame",
            "A=M-1",
            "A=A-1",
            "A=A-1",
            "A=A-1",
            "D=M",
            "@LCL",
            "M=D",
            # goto retAddr
            f"@retAddr",
            "A=M",
            "0;JMP",
        ]
        return "\n".join(command_lines)


class UnrecognisedCmdError(Exception):
    pass
