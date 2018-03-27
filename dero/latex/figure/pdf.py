from dero.latex.figure.models import Subfigure, Figure
from dero.latex.models import Document

def filepaths_to_figure_pdf(filepaths, subfigure_kwargs={}, figure_kwargs={}):
    subfigures = [Subfigure(fp, **subfigure_kwargs) for fp in filepaths]
    figure = Figure(subfigures, **figure_kwargs)

    package_strs = [
        'caption',
        'subcaption',
        'graphicx'
    ]

    document = Document(
        package_strs,
        figure
    )

    return document
