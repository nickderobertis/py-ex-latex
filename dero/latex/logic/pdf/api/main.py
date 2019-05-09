from data import Data
import latex
from latex.exc import LatexBuildError
from dero.latex.logic.pdf.errors.exc import TooManyUnprocessedFloatsException, LatexException, exception_manager


def latex_str_to_pdf_obj(latex_str: str) -> Data:

    try:
        return _latex_to_pdf_obj(latex_str)
    except LatexBuildError as e:
        exceptions = exception_manager.exceptions_from_latex_build_error(e)
        exceptions_to_raise = []
        for exception in exceptions:
            try:
                raise exception
            except TooManyUnprocessedFloatsException:
                print('got unprocessed floats')
            except Exception as e:
                exceptions_to_raise.append(e)
        if exceptions_to_raise:
            raise LatexException(exceptions_to_raise)


def _latex_to_pdf_obj(latex_str: str) -> Data:
    pdf = latex.build_pdf(latex_str)
    return pdf

