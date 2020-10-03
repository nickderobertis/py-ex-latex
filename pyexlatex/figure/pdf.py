import posixpath

from pyexlatex.figure.models import Subfigure, Figure
from pyexlatex.logic.output.main import output_document_and_move
from pyexlatex.texgen.replacements.filename import _latex_valid_basename
from pyexlatex.models.document import Document
from pyexlatex.models.package import Package


def filepaths_to_pdf_figure_and_move(filepaths,  outfolder, outname='figure', as_document=True,
                                     subfigure_kwargs={}, figure_kwargs={}, document_kwargs={}):

    basenames = [_latex_valid_basename(filepath) for filepath in filepaths]
    sources_paths = [posixpath.join('Sources', basename) for basename in basenames]

    document_or_figure = _filepaths_to_document_or_figure(
        sources_paths,
        subfigure_kwargs=subfigure_kwargs,
        figure_kwargs=figure_kwargs,
        document_kwargs=document_kwargs,
        as_document=as_document
    )

    output_document_and_move(
        document_or_figure,
        outfolder,
        image_paths=filepaths,
        outname=outname,
        as_document=as_document
    )

    return document_or_figure


def _filepaths_to_document_or_figure(filepaths, subfigure_kwargs={}, figure_kwargs={}, document_kwargs={},
                                     as_document=True):
    subfigures = [Subfigure(fp, **subfigure_kwargs) for fp in filepaths]
    figure = Figure(subfigures, **figure_kwargs)

    if not as_document:
        return figure

    simple_package_strs = [
        'caption',
        'subcaption',
        'graphicx',
        'pdflscape'
    ]
    simple_packages = [Package(str_) for str_ in simple_package_strs]

    packages = simple_packages + []  # add any packages with options here with the Package class

    document = Document(
        figure,
        packages,
        **document_kwargs
    )

    return document

