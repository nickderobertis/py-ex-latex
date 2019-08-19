from typing import Optional, List, Dict, Any
import warnings
from data import Data
import latex
from latex.exc import LatexBuildError
from pyexlatex.logic.pdf.errors.exc import (
    TooManyUnprocessedFloatsException,
    OutputLoopConsecutiveDeadCycles,
    LatexException,
    exception_manager
)
from pyexlatex.logic.pdf.api.exc_handler.main import APIExceptionHandler
from pyexlatex.logic.pdf.api.exc_handler.prepend.typing import PrependKwargsDict, PrependItemsDict
from pyexlatex.logic.pdf.api.exc_handler.prepend.main import add_prepend_items_dict_to_latex_str
from pyexlatex.logic.pdf.api.builders.lualatex import LuaLatexBuilder

def latex_str_to_pdf_obj(latex_str: str, texinputs: Optional[List[str]] = None, run_bibtex: bool = False,
                         retries_remaining: int = 3,
                         prepend_items_dict: PrependItemsDict = None,
                         prepend_kwargs_dict: PrependKwargsDict = None) -> Data:
    try:
        new_latex_str = add_prepend_items_dict_to_latex_str(prepend_items_dict, latex_str)
        return _latex_to_pdf_obj(new_latex_str, texinputs=texinputs, run_bibtex=run_bibtex)
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
            run_bibtex=run_bibtex
        )
        return handler.handle_exceptions()


def _latex_to_pdf_obj(latex_str: str, texinputs: Optional[List[str]] = None,
                      run_bibtex: bool = False) -> Data:
    if texinputs is None:
        texinputs = []
    pdf = LuaLatexBuilder().build_pdf(latex_str, texinputs=texinputs, run_bibtex=run_bibtex)
    return pdf

