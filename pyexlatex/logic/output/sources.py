import os
from typing import Optional, List

from pyexlatex.logic.output.fileops import _copy_if_needed
from pyexlatex.texgen.replacements.filename import _latex_valid_basename
from pyexlatex.typing import StrListOrNone, BytesListOrNone, StrList, BytesList


def output_sources_return_tex_input_paths(outfolder: str, image_paths: StrListOrNone = None,
                                          image_binaries: BytesListOrNone = None) -> Optional[List[str]]:
    tex_inputs: Optional[List[str]]
    if image_paths:
        # Copy first time for creation of pdf
        sources_tempfolder = os.path.join(outfolder, 'Sources')
        tex_inputs = [os.path.abspath(outfolder), os.path.abspath(sources_tempfolder), '.']
        if not os.path.exists(sources_tempfolder):
            os.makedirs(sources_tempfolder)
        if image_binaries:
            _write_image_paths_and_binaries_to_folder(sources_tempfolder, image_paths, image_binaries)
        else:
            [_copy_if_needed(filepath, os.path.join(sources_tempfolder, _latex_valid_basename(filepath)))
             for filepath in image_paths]
    else:
        tex_inputs = None

    return tex_inputs


def _write_image_paths_and_binaries_to_folder(folder: str, image_paths: StrList, image_binaries: BytesList):
    if len(image_binaries) != len(image_paths):
        raise ValueError('must have equal image_binaries and image_path lengths if image_binaries are passed')
    for filepath, binary in zip(image_paths, image_binaries):
        image_outpath = os.path.join(folder, _latex_valid_basename(filepath))
        with open(image_outpath, 'wb') as f:
            f.write(binary)