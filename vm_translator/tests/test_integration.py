from pathlib import Path
from unittest.mock import patch
import pytest
import os
from vm_translator.VMTranslator import Compiler
import filecmp

OUTPUT_FILE = Path("SimpleAddReference.asm")
resource_dir = Path(os.path.dirname(__file__)) / "resources/"


def test_pointer_vm_file_is_properly_compiled(mockdata_time_and_remove_output_file):
    reference_file = resource_dir / "PointerTestReference.asm"
    pointer_test_vm_file = resource_dir / "PointerTest.vm"

    compiler = Compiler(pointer_test_vm_file, OUTPUT_FILE)
    compiler.compile_and_write_asm()

    assert filecmp.cmp(reference_file, OUTPUT_FILE) is True


def test_simple_add_vm_file_is_properly_compiled(mockdata_time_and_remove_output_file):
    reference_file = resource_dir / "SimpleAddReference.asm"
    pointer_test_vm_file = resource_dir / "SimpleAdd.vm"

    compiler = Compiler(pointer_test_vm_file, OUTPUT_FILE)
    compiler.compile_and_write_asm()

    assert filecmp.cmp(reference_file, OUTPUT_FILE) is True


@pytest.fixture
def mockdata_time_and_remove_output_file():
    with patch("vm_translator.code_writer.datetime") as mocked_datatime:
        mocked_datatime.today.return_value = "2023-01-17 17:05:03.561633"
        yield
    os.remove(OUTPUT_FILE)
