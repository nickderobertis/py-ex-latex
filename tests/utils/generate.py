from pathlib import Path
from typing import Final

from pyexlatex.models.document import DocumentBase
from pyexlatex.typing import PyexlatexItem
from tests.base import INPUT_TABLES_DIR, INPUT_DOCUMENTS_DIR, INPUT_PRESENTATIONS_DIR

GENERATE_MODE: Final = False


def _assert_same_or_generate(content: str, path: Path):
    if GENERATE_MODE:
        path.write_text(content)
        return
    expect_content = path.read_text()
    assert content == expect_content


def assert_same_or_generate_table(content: PyexlatexItem, name: str):
    path = INPUT_TABLES_DIR / f"{name}.tex"
    _assert_same_or_generate(str(content), path)


def assert_same_or_generate_document(content: DocumentBase, name: str):
    path = INPUT_DOCUMENTS_DIR / f"{name}.tex"
    _assert_same_or_generate(str(content), path)


def assert_same_or_generate_presentation(content: DocumentBase, name: str):
    path = INPUT_PRESENTATIONS_DIR / f"{name}.tex"
    _assert_same_or_generate(str(content), path)