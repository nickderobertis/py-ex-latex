import os
import posixpath
import shutil

from dero.latex.figure.models import Subfigure, Figure
from dero.latex.models import Document, Package
from dero.latex.tools import date_time_move_latex

def filepaths_to_pdf_figure_and_move(filepaths,  outfolder, outname='figure', as_document=True,
                                     subfigure_kwargs={}, figure_kwargs={}, document_kwargs={}):

    basenames = [_latex_valid_basename(filepath) for filepath in filepaths]
    sources_paths = [posixpath.join('Sources', basename) for basename in basenames]

    document = _filepaths_to_document(
        sources_paths,
        subfigure_kwargs=subfigure_kwargs,
        figure_kwargs=figure_kwargs,
        document_kwargs=document_kwargs
    )

    _document_to_pdf_and_move(
        document,
        outfolder,
        image_paths=filepaths,
        outname=outname,
        as_document=as_document
    )

    return document

def _document_to_pdf_and_move(document, outfolder, image_paths=None, outname='figure', as_document=True):

    # We will change paths, so save original to switch back to
    orig_path = os.getcwd()

    os.chdir(outfolder)

    # Create tex file
    outname_tex = outname + '.tex'
    with open(outname_tex, 'w') as f:
        f.write(str(document))

    if image_paths:
        # Copy first time for creation of pdf
        sources_tempfolder = os.path.join(outfolder, 'Sources')
        if not os.path.exists(sources_tempfolder):
            os.makedirs(sources_tempfolder)
        [_copy_if_needed(filepath, os.path.join(sources_tempfolder, _latex_valid_basename(filepath)))
         for filepath in image_paths]

    if as_document:
        os.system('pdflatex ' + '"' + outname_tex + '"') #create PDF
    new_outfolder = date_time_move_latex(outname, outfolder, folder_name='Figures') #move table into appropriate date/number folder
    sources_outfolder = os.path.join(new_outfolder, 'Sources')

    if image_paths and new_outfolder:
        # Copy second time to move pictures along with pdf
        _move_if_needed(sources_tempfolder, sources_outfolder)

    os.chdir(orig_path)

def _filepaths_to_document(filepaths, subfigure_kwargs={}, figure_kwargs={}, document_kwargs={}):
    subfigures = [Subfigure(fp, **subfigure_kwargs) for fp in filepaths]
    figure = Figure(subfigures, **figure_kwargs)

    simple_package_strs = [
        'caption',
        'subcaption',
        'graphicx',
        'pdflscape'
    ]
    simple_packages = [Package(str_) for str_ in simple_package_strs]

    packages = simple_packages + [
        Package('geometry', modifier_str='margin=0.1in')
    ]

    document = Document(
        packages,
        figure,
        **document_kwargs
    )

    return document

def _copy_if_needed(src, dst):
    try:
        shutil.copy(src, dst)
    except shutil.SameFileError:
        pass

def _move_if_needed(src, dst):
    try:
        shutil.move(src, dst)
    except shutil.SameFileError:
        pass

def _move_folder_or_move_files_if_destination_folder_exists(src, dst):
    try:
        _move_if_needed(src, dst)
    except shutil.Error:
        files = [file for file in next(os.walk(src))[2]]
        [_move_if_needed(file, dst) for file in files]

def _latex_valid_basename(filepath):
    basename = os.path.basename(filepath)
    return basename.replace(' ', '_').replace('/','_').replace('%','pct')