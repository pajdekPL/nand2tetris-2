from sys import argv
from pathlib import Path

from vm_translator.code_writer import CodeWriter
from vm_translator.parser import Parser


class Compiler:
    def __init__(self, vm_file_path: Path, asm_output_file_path=None):
        self.vm_file_path = vm_file_path

        if not asm_output_file_path:
            self.asm_file_path = Path(str(vm_file_path).replace('.vm', '.asm'))
        else:
            self.asm_file_path = asm_output_file_path

        self.parser = Parser(self.vm_file_path)
        self.writer = CodeWriter(self.asm_file_path)

    def compile_and_write_asm(self):
        for cmd in self.parser:
            self.writer.write_cmd(cmd)
        self.writer.close_file()


if __name__ == "__main__":
    if len(argv) < 2:
        raise IOError("Please pass path to the VM file that should be complied to ASM")
    file_path = Path(argv[1])
    compiler = Compiler(file_path)
    compiler.compile_and_write_asm()

