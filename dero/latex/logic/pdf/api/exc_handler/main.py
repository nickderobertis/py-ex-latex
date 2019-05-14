from typing import List, Optional, Dict, Any
import warnings
from dero.latex.logic.pdf.errors.exc import (
    LatexException
)
from dero.latex.logic.pdf.api.exc_handler.prepend.main import handle_prepend_exceptions
from dero.latex.logic.pdf.api.exc_handler.prepend.typing import PrependKwargsDict, PrependItemsDict


class APIExceptionHandler:

    def __init__(self, exceptions: List[LatexException], orig_exception: Exception, latex_str: str,
                 prepend_kwargs_dict: PrependKwargsDict = None, prepend_items_dict: PrependItemsDict = None,
                 retries_remaining: int = 3):
        self.exceptions = exceptions
        self.orig_exception = orig_exception
        self.latex_str = latex_str
        self.prepend_kwargs_dict = prepend_kwargs_dict
        self.prepend_items_dict = prepend_items_dict
        self.retries_remaining = retries_remaining

    def handle_exceptions(self):
        from dero.latex.logic.pdf.api.main import latex_str_to_pdf_obj
        if not self.exceptions:
            # Got LatexBuildError, but could not extract any exceptions from it. Something is going wrong
            # Seems like it might be some intermittent issue, try retrying
            if self.retries_remaining > 0:
                warnings.warn('got empty latex build error. trying to create pdf again')
                return latex_str_to_pdf_obj(
                    self.latex_str,
                    retries_remaining=self.retries_remaining - 1,
                    prepend_items_dict=self.prepend_items_dict,
                    prepend_kwargs_dict=self.prepend_kwargs_dict
                )
            raise LatexException(self.orig_exception)
        prepend_items_dict, prepend_kwarg_dict, unhandled_exceptions = handle_prepend_exceptions(
            self.exceptions, self.prepend_kwargs_dict, self.prepend_items_dict
        )

        # TODO: handle other exceptions

        if len(unhandled_exceptions) == len(self.exceptions):
            # was not able to handle any exceptions, so retrying would be of no use
            raise LatexException(self.exceptions)

        return latex_str_to_pdf_obj(
            self.latex_str,
            retries_remaining=self.retries_remaining,
            prepend_items_dict=prepend_items_dict,
            prepend_kwargs_dict=prepend_kwarg_dict
        )






