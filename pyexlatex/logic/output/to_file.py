from tempdir import TempDir

from pyexlatex.logic.output.api.main import latex_str_to_obj
from pyexlatex.logic.output.api.formats import OutputFormats
from pyexlatex.logic.output.sources import output_sources_return_tex_input_paths
from pyexlatex.typing import StrListOrNone, BytesListOrNone


def latex_str_to_file(latex_str: str, filepath: str, output_format: OutputFormats = OutputFormats.PDF,
                      texinputs: StrListOrNone = None,
                      run_bibtex: bool = False):
    obj = latex_str_to_obj(latex_str, output_format=output_format, texinputs=texinputs, run_bibtex=run_bibtex)
    obj.save_to(filepath)
    return obj


def latex_str_to_file_obj_with_sources(latex_str: str, output_format: OutputFormats = OutputFormats.PDF,
                                       image_paths: StrListOrNone = None,
                                       image_binaries: BytesListOrNone = None, run_bibtex: bool = False):
    with TempDir() as tmpdir:
        tex_inputs = output_sources_return_tex_input_paths(
            tmpdir, image_paths=image_paths, image_binaries=image_binaries
        )
        obj = latex_str_to_obj(latex_str, output_format=output_format, texinputs=tex_inputs, run_bibtex=run_bibtex)

    return obj