from pathlib import Path
from unittest.mock import patch
import pytest
import os
from vm_translator.VMTranslator import Compiler
import filecmp

OUTPUT_FILE = Path("output_file.asm")
resource_dir = Path(os.path.dirname(__file__)) / "resources/"


@pytest.mark.parametrize(
    "input_vm_file, reference_file",
    [
        (resource_dir / "PointerTest.vm", resource_dir / "PointerTestReference.asm"),
        (resource_dir / "SimpleAdd.vm", resource_dir / "SimpleAddReference.asm"),
        (
            resource_dir / "FibonacciSeries.vm",
            resource_dir / "FibonacciSeriesReference.asm",
        ),
        (
            resource_dir / "nested_call",
            resource_dir / "nested_call/NestedCallReference.asm",
        ),
    ],
)
def test_pointer_vm_file_is_properly_compiled(
    mockdata_time_and_remove_output_file, input_vm_file, reference_file
):
    compiler = Compiler(input_vm_file, OUTPUT_FILE)
    compiler.compile_and_write_asm()

    assert filecmp.cmp(reference_file, OUTPUT_FILE) is True


@pytest.fixture
def mockdata_time_and_remove_output_file():
    with patch("vm_translator.code_writer.datetime") as mocked_datatime:
        mocked_datatime.today.return_value = "2023-01-17 17:05:03.561633"
        yield
    os.remove(OUTPUT_FILE)
