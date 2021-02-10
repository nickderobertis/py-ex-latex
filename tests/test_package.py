import pyexlatex as pl
from pyexlatex.texgen.packages.default import default_packages
from tests.base import GENERATED_FILES_DIR, INPUT_FILES_DIR
from tests.utils.pdf import compare_pdfs


def test_package():
    package = pl.Package('hyperref', modifier_str='hidelinks')
    assert str(package) == '\\usepackage[hidelinks]{hyperref}'


def test_require_package():
    package = pl.RequirePackage('hyperref', modifier_str='hidelinks')
    assert str(package) == '\\RequirePackage[hidelinks]{hyperref}'


def test_package_conflict():
    section = pl.Section(['woo'], title='Section')
    section.init_data()
    section.add_package(pl.Package('hyperref', modifier_str='hidelinks'))
    # Without eq_on_modifier=False, raises error for package options conflict
    section.add_package(pl.Package('hyperref', modifier_str='linktoc=all', eq_on_modifier=False))
    doc = pl.Document([section])
    doc.to_pdf(GENERATED_FILES_DIR, outname='package conflict document')
    compare_pdfs(INPUT_FILES_DIR / 'package conflict document.pdf', GENERATED_FILES_DIR / 'package conflict document.pdf')


def test_package_conflict_with_document_packages():
    section = pl.Section(['woo'], title='Section')
    section.init_data()
    # Without eq_on_modifier=False, raises error for package options conflict
    section.add_package(pl.Package('hyperref', modifier_str='linktoc=all', eq_on_modifier=False))

    doc = pl.Document([section], packages=default_packages + [pl.Package('hyperref', modifier_str='hidelinks')])
    doc.to_pdf(GENERATED_FILES_DIR, outname='package conflict document')
    compare_pdfs(INPUT_FILES_DIR / 'package conflict document.pdf',
                 GENERATED_FILES_DIR / 'package conflict document.pdf')
