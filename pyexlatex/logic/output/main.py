import os

from pyexlatex.logic.output.api.formats import OutputFormats
from pyexlatex.logic.output.to_file import latex_str_to_file
from pyexlatex.logic.output.sources import output_sources_return_tex_input_paths, \
    _write_image_paths_and_binaries_to_folder
from pyexlatex.tools import date_time_move_latex
from pyexlatex.logic.output.fileops import _move_if_exists_and_is_needed
from pyexlatex.texgen.replacements.filename import _latex_valid_basename
from pyexlatex.typing import BytesListOrNone, StrListOrNone


def output_document_and_move(document, outfolder, output_format: OutputFormats = OutputFormats.PDF,
                             image_paths: StrListOrNone = None, outname='figure', as_document=True,
                             move_folder_name='Figures', image_binaries: BytesListOrNone = None,
                             run_bibtex: bool = False, date_time_move: bool = False):

    # Create tex file
    outname_tex = outname + '.tex'
    outpath_tex = os.path.abspath(os.path.join(outfolder, outname_tex))
    with open(outpath_tex, 'w', encoding='utf8') as f:
        f.write(str(document))

    tex_inputs = output_sources_return_tex_input_paths(
        outfolder, image_paths=image_paths, image_binaries=image_binaries
    )

    if as_document:
        outname_final = outname + f'.{output_format.value}'
        outpath_final = os.path.abspath(os.path.join(outfolder, outname_final))
        latex_str_to_file(
            str(document), outpath_final, output_format=output_format, texinputs=tex_inputs, run_bibtex=run_bibtex
        )
    if not date_time_move:
        return

    # Handle date/time move functionality
    new_outfolder = date_time_move_latex(outname, outfolder, folder_name=move_folder_name) #move table into appropriate date/number folder

    if image_paths and new_outfolder:
        # Copy second time to move pictures along with pdf
        sources_tempfolder = os.path.join(outfolder, 'Sources')
        sources_outfolder = os.path.join(new_outfolder, 'Sources')
        if not os.path.exists(sources_outfolder):
            os.makedirs(sources_outfolder)
        if image_binaries:
            _write_image_paths_and_binaries_to_folder(sources_outfolder, image_paths, image_binaries)
        else:
            [_move_if_exists_and_is_needed(
                os.path.join(sources_tempfolder, _latex_valid_basename(filepath)),
                os.path.join(sources_outfolder, _latex_valid_basename(filepath))
             )
            for filepath in image_paths]
