import fitz

from tests.base import INPUT_FILES_DIR, GENERATED_FILES_DIR


def compare_pdfs_in_generated_vs_input_by_name(name: str):
    generated_file = GENERATED_FILES_DIR / f'{name}.pdf'
    input_file = INPUT_FILES_DIR / f'{name}.pdf'
    compare_pdfs(generated_file, input_file)


def compare_pdfs(path_a: str, path_b: str):
    """
    Asserts that two PDFs are equal by loading them from file
    and checking content.

    This is necessary instead of simply comparing bytes because
    the order of certain items in the PDF bytes is not
    guaranteed.

    See https://github.com/rst2pdf/rst2pdf/blob/master/rst2pdf/tests/conftest.py

    :param path_a:
    :param path_b:
    :return:
    """
    pdf_a = fitz.open(path_a)
    pdf_b = fitz.open(path_b)

    # sanity check

    assert pdf_a.isPDF
    assert pdf_b.isPDF

    # compare metadata

    assert _get_metadata(pdf_a) == _get_metadata(pdf_b)

    # compare content

    pages_a = _get_pages(pdf_a)
    pages_b = _get_pages(pdf_b)

    def fuzzy_coord_diff(coord_a, coord_b):
        diff = abs(coord_a - coord_b)
        assert diff / max(coord_a, coord_b) < 0.04  # allow an arbitrary diff

    def fuzzy_string_diff(string_a, string_b):
        words_a = string_a.split()
        words_b = string_a.split()
        assert words_a == words_b

    assert len(pages_a) == len(pages_b)
    for page_a, page_b in zip(pages_a, pages_b):
        assert len(page_a) == len(page_b)
        for block_a, block_b in zip(page_a, page_b):
            # each block has the following format:
            #
            # (x0, y0, x1, y1, "lines in block", block_type, block_no)
            #
            # block_type and block_no should remain unchanged, but it's
            # possible for the blocks to move around the document slightly and
            # the text refold without breaking entirely
            fuzzy_coord_diff(block_a[0], block_b[0])
            fuzzy_coord_diff(block_a[1], block_b[1])
            fuzzy_coord_diff(block_a[2], block_b[2])
            fuzzy_coord_diff(block_a[3], block_b[3])
            fuzzy_string_diff(block_a[4], block_b[4])
            assert block_a[5] == block_b[5]
            assert block_a[6] == block_b[6]


def _get_metadata(pdf):
    metadata = pdf.metadata

    del metadata["creationDate"]
    del metadata["modDate"]

    return metadata


def _get_pages(pdf):
    pages = []

    for page in pdf.pages():
        pages.append(page.getText("blocks"))

    return pages
