from typing import List, Dict, TYPE_CHECKING, Type

if TYPE_CHECKING:
    from pyexlatex.logic.output.errors.exc import LatexException
from pyexlatex.logic.output.errors.models.error import LatexError
from pyexlatex.logic.output.errors.models.error_collection import LatexErrorCollection
from latex.exc import LatexBuildError


class LatexExceptionManager:

    def __init__(self, exceptions: List[Type['LatexException']]):
        self.exceptions_list = exceptions
        self.exceptions = self._create_map()
        self.match_strs = [key for key in self.exceptions.keys()]

    def _create_map(self) -> Dict[str, Type['LatexException']]:
        exception_map = {}
        for exc in self.exceptions_list:
            exception_map[exc._match_str] = exc
        return exception_map

    def exception_from_error(self, error: LatexError) -> 'LatexException':
        from pyexlatex.logic.output.errors.exc import LatexException
        for possible_match in self.match_strs:
            if possible_match in error.error:
                exc_class = self.exceptions[possible_match]
                return exc_class(error.error)

        # No match found, return general exception
        return LatexException(error.error)

    def exceptions_from_latex_build_error(self, build_error: LatexBuildError) -> List['LatexException']:
        errors = LatexErrorCollection(build_error)
        return [self.exception_from_error(latex_error) for latex_error in errors]
