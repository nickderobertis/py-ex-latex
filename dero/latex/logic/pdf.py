import os
import shutil

from dero.latex.tools import date_time_move_latex


def _document_to_pdf_and_move(document, outfolder, image_paths=None, outname='figure', as_document=True,
                              move_folder_name='Figures'):

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
    new_outfolder = date_time_move_latex(outname, outfolder, folder_name=move_folder_name) #move table into appropriate date/number folder

    if image_paths and new_outfolder:
        # Copy second time to move pictures along with pdf
        sources_outfolder = os.path.join(new_outfolder, 'Sources')
        _move_if_needed(sources_tempfolder, sources_outfolder)

    os.chdir(orig_path)


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