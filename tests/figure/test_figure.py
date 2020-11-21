import pandas as pd

import pyexlatex as pl
from tests.base import EXAMPLE_IMAGE_PATH, GENERATED_FILES_DIR
from tests.utils.pdf import compare_pdfs_in_generated_vs_input_by_name


def test_single_figure_from_graphic():
    graphic = pl.Graphic(str(EXAMPLE_IMAGE_PATH))
    fig = pl.Figure([graphic])
    assert str(fig) == '\\begin{figure}\n\\includegraphics[width=1.0\\textwidth]{Sources/nd-logo.png}\n\\end{figure}'
    fig = pl.Figure([graphic], position_str='[h!]')
    assert str(fig) == '\\begin{figure}\n[h!]\n\\includegraphics[width=1.0\\textwidth]{Sources/nd-logo.png}\n\\end{figure}'
    fig = pl.Figure([graphic], caption='image')
    assert str(fig) == '\\begin{figure}\n\\includegraphics[width=1.0\\textwidth]{Sources/nd-logo.png}\n\\caption{image}\n\\end{figure}'
    fig = pl.Figure.from_dict_of_names_and_filepaths({'image': str(EXAMPLE_IMAGE_PATH)})
    assert str(fig) == '\\begin{figure}\n\\includegraphics[width=0.45\\linewidth]{Sources/nd-logo.png}\n\\caption{image}\n\\end{figure}'
    fig = pl.Figure([graphic], caption='woo', label='yeah', centering=False, landscape=True, position_str=r'[h!]')
    assert str(fig) == '\\begin{lfigure}\n[h!]\n\\includegraphics[width=1.0\\textwidth]{Sources/nd-logo.png}\n\\caption{woo}\n\\label{yeah}\n\\end{lfigure}'
    name = 'figure from single graphic document'
    fig.to_pdf_and_move(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_subfigure_graphic():
    subf1 = pl.Subfigure(str(EXAMPLE_IMAGE_PATH))
    subf2 = pl.Subfigure(str(EXAMPLE_IMAGE_PATH))
    fig = pl.Figure([subf1, subf2])
    assert str(fig) == '\\begin{figure}\n\\centering\n\\begin{subfigure}\n[t]{0.45\\linewidth}\n\\centering\n\\includegraphics[width=1.0\\textwidth]{Sources/nd-logo.png}\n\\end{subfigure}\n\\begin{subfigure}\n[t]{0.45\\linewidth}\n\\centering\n\\includegraphics[width=1.0\\textwidth]{Sources/nd-logo.png}\n\\end{subfigure}\n\\end{figure}'


def test_figure_from_matplotlib():
    plot = pd.Series([1, 2, 3, 4]).plot().get_figure()
    fig = pl.Figure.from_dict_of_names_and_plt_figures({'plot': plot}, GENERATED_FILES_DIR)
    assert str(fig) == '\\begin{figure}\n\\includegraphics[width=0.45\\linewidth]{Sources/plot.pdf}\n\\caption{plot}\n\\end{figure}'
    name = 'figure from matplotlib'
    fig.to_pdf_and_move(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)
    fig = pl.Figure.from_dict_of_names_and_plt_figures({'plot': plot}, GENERATED_FILES_DIR, position_str='[h!]')
    assert str(fig) == '\\begin{figure}\n[h!]\n\\includegraphics[width=0.45\\linewidth]{Sources/plot.pdf}\n\\caption{plot}\n\\end{figure}'


def test_graphic_from_single_graphic_figure():
    graphic = pl.Graphic(str(EXAMPLE_IMAGE_PATH))
    fig = pl.Figure([graphic])
    graphics = fig.to_graphic_list()
    assert str(graphic) == str(graphics[0])
    assert len(graphics) == 1


def test_graphics_from_multiple_subfigure_figure():
    graphic = pl.Graphic(str(EXAMPLE_IMAGE_PATH))
    subf1 = pl.Subfigure(str(EXAMPLE_IMAGE_PATH))
    subf2 = pl.Subfigure(str(EXAMPLE_IMAGE_PATH))
    fig = pl.Figure([subf1, subf2])
    graphics = fig.to_graphic_list()
    assert len(graphics) == 2
    for g in graphics:
        assert str(graphic) == str(g)