import pandas as pd

import pyexlatex as pl

from tests.base import GENERATED_FILES_DIR, EXAMPLE_IMAGE_PATH
from tests.utils.generate import assert_same_or_generate_presentation
from tests.utils.pdf import compare_pdfs_in_generated_vs_input_by_name


def test_basic_presentation():
    doc = pl.Presentation(['woo'])
    name = 'basic presentation'
    assert_same_or_generate_presentation(doc, name)
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_presentation_options():
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            'woo'
                        ],
                        title='One-One'
                    ),
                    pl.Frame(
                        [
                            'woo2'
                        ],
                        title='One-Two'
                    )
                ],
                title="One"
            ),
            pl.Section(
                [
                    pl.Frame(
                        [
                            'woo3'
                        ],
                        title='Two-One'
                    ),
                    pl.Frame(
                        [
                            'woo4'
                        ],
                        title='Two-Two'
                    )
                ],
                title="Two"
            )
        ],
        packages=['hyperref'],
        title='Test Presentation',
        authors=['Nick DeRobertis', 'Someone Else'],
        date='2020-10-19',
        short_title='Pres',
        subtitle='A Presentation for Testing Purposes',
        short_author='People',
        institutions=[['University of Florida', 'Line two'], ['Virginia Commonwealth University']],
        short_institution='UF & VCU',
        font_size=15,
        nav_header=True,
        toc_sections=True,
    )
    name = 'presentation with options'
    assert_same_or_generate_presentation(doc, name)
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_table_in_presentation():
    df = pd.DataFrame(
        [
            (1, 2, 3.546),
            (4, 5, 66546.4),
            (7, 8, 96.54)
        ],
        columns=['a', 'b', 'c']
    )
    table = pl.Table.from_list_of_lists_of_dfs(
        [[df]],
        caption='My Table Title',
        below_text='My below text',
        align='L{5cm}c.',
        mid_rules=False,
    )
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            table
                        ],
                        title='Table'
                    ),
                ],
                title="Section"
            ),
        ],
    )
    name = 'presentation with table'
    assert_same_or_generate_presentation(doc, name)
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_tabular_from_table_in_presentation():
    df = pd.DataFrame(
        [
            (1, 2, 3.546),
            (4, 5, 66546.4),
            (7, 8, 96.54)
        ],
        columns=['a', 'b', 'c']
    )
    table = pl.Table.from_list_of_lists_of_dfs(
        [[df], [df + 10]],
        caption='My Table Title',
        below_text='My below text',
        align='L{5cm}c.'
    )
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            table.tex_obj(as_document=False, as_single_tabular=True),
                        ],
                        title='Tabular'
                    ),
                ],
                title="Section"
            ),
        ],
    )
    name = 'presentation with tabular'
    assert_same_or_generate_presentation(doc, name)
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_tabular_list_from_table_in_presentation():
    df = pd.DataFrame(
        [
            (1, 2, 3.546),
            (4, 5, 66546.4),
            (7, 8, 96.54)
        ],
        columns=['a', 'b', 'c']
    )
    table = pl.Table.from_list_of_lists_of_dfs(
        [[df], [df + 10]],
        caption='My Table Title',
        below_text='My below text',
        align='L{5cm}c.'
    )
    frames = [
        pl.Frame(tab, title=f'Tabular {i + 1}')
        for i, tab in enumerate(table.tex_obj(as_document=False, as_panel_tabular_list=True))
    ]

    doc = pl.Presentation(
        [
            pl.Section(
                [
                    frames,
                ],
                title="Section"
            ),
        ],
    )
    name = 'presentation with tabular list'
    assert_same_or_generate_presentation(doc, name)
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_figure_in_presentation():
    graphic = pl.Graphic(str(EXAMPLE_IMAGE_PATH), width=0.4)
    fig = pl.Figure([graphic], caption='My Figure')
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            fig
                        ],
                        title='Figure'
                    ),
                ],
                title="Section"
            ),
        ],
    )
    name = 'presentation with figure'
    assert_same_or_generate_presentation(doc, name)
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_graphic_from_figure_in_presentation():
    graphic = pl.Graphic(str(EXAMPLE_IMAGE_PATH), width=0.4)
    fig = pl.Figure([graphic], caption='My Figure')
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            fig.to_graphic_list()[0]
                        ],
                        title='Graphic'
                    ),
                ],
                title="Section"
            ),
        ],
    )
    name = 'presentation with graphic from figure'
    assert_same_or_generate_presentation(doc, name)
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)