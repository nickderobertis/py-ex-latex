from typing import Optional, List, Dict, Type
from data import Data
from latex.exc import LatexBuildError

from pyexlatex.logic.output.api.builders.base import BaseBuilder
from pyexlatex.logic.output.api.builders.htlatex import HTLatexBuilder
from pyexlatex.logic.output.api.formats import OutputFormats
from pyexlatex.logic.output.errors.exc import (
    exception_manager
)
from pyexlatex.logic.output.api.exc_handler.main import APIExceptionHandler
from pyexlatex.logic.output.api.exc_handler.prepend.typing import PrependKwargsDict, PrependItemsDict
from pyexlatex.logic.output.api.exc_handler.prepend.main import add_prepend_items_dict_to_latex_str
from pyexlatex.logic.output.api.builders.lualatex import LuaLatexBuilder

BUILDERS: Dict[OutputFormats, Type[BaseBuilder]] = {
    OutputFormats.PDF: LuaLatexBuilder,
    OutputFormats.HTML: HTLatexBuilder,
}


def latex_str_to_obj(latex_str: str, output_format: OutputFormats = OutputFormats.PDF,
                     texinputs: Optional[List[str]] = None, run_bibtex: bool = False,
                     retries_remaining: int = 3,
                     prepend_items_dict: PrependItemsDict = None,
                     prepend_kwargs_dict: PrependKwargsDict = None) -> Data:
    try:
        new_latex_str = add_prepend_items_dict_to_latex_str(prepend_items_dict, latex_str)
        return _latex_to_obj(new_latex_str, output_format, texinputs=texinputs, run_bibtex=run_bibtex)
    except LatexBuildError as e:
        exceptions = exception_manager.exceptions_from_latex_build_error(e)
        handler = APIExceptionHandler(
            exceptions,
            e,
            latex_str,
            prepend_kwargs_dict=prepend_kwargs_dict,
            prepend_items_dict=prepend_items_dict,
            retries_remaining=retries_remaining,
            texinputs=texinputs,
            run_bibtex=run_bibtex,
            output_format=output_format,
        )
        return handler.handle_exceptions()


def _latex_to_obj(latex_str: str, output_format: OutputFormats, texinputs: Optional[List[str]] = None,
                  run_bibtex: bool = False) -> Data:
    if texinputs is None:
        texinputs = []
    builder = BUILDERS[output_format]
    obj = builder().build(latex_str, texinputs=texinputs, run_bibtex=run_bibtex)
    return obj


