from sys import argv
from pathlib import Path

from vm_translator.code_writer import CodeWriter
from vm_translator.parser import Parser


class Compiler:
    def __init__(self, vm_path: Path, asm_output_file_path: Path = None):
        self.vm_path = vm_path
        self.is_dir = self.vm_path.is_dir()
        if not asm_output_file_path:
            self.asm_file_path = self.get_asm_file_name()
        else:
            self.asm_file_path = asm_output_file_path

    def compile_and_write_asm(self):
        if not self.is_dir:
            self._compile_and_write_single_vm_file()
            return
        self._compile_and_write_dir()

    def _compile_and_write_single_vm_file(self):
        writer = CodeWriter(self.asm_file_path)
        parser = Parser(self.vm_path)
        for cmd in parser:
            writer.write_cmd(cmd)
        writer.close_file()

    def _compile_and_write_dir(self):
        writer = CodeWriter(self.asm_file_path, True)
        for vm_file in self.vm_path.glob("**/*.vm"):
            parser = Parser(vm_file)
            for cmd in parser:
                writer.file_name = vm_file.name
                writer.write_cmd(cmd)
        writer.close_file()

    def get_asm_file_name(self):
        if self.is_dir:
            return self.vm_path / f"{self.vm_path.name}.asm"
        return Path(str(self.vm_path).replace("vm", "asm"))


if __name__ == "__main__":
    if len(argv) < 2:
        raise IOError("Please pass path to the VM file that should be complied to ASM")
    file_path = Path(argv[1])
    compiler = Compiler(file_path)
    compiler.compile_and_write_asm()
