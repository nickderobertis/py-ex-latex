from typing import List
from latex.exc import LatexBuildError
from dero.latex.logic.pdf.errors.models.error import LatexError


class LatexErrorCollection:

    def __init__(self, latex_build_error: LatexBuildError):
        self.exc = latex_build_error
        self.errors = self._parse_errors()

    def __getitem__(self, index):
        return self.errors[index]

    def _parse_errors(self) -> List[LatexError]:
        error_dict_list = self.exc.get_errors()
        errors = []
        for error_dict in error_dict_list:
            arg_dict = error_dict.copy()
            arg_dict.pop('error')
            errors.append(LatexError(**arg_dict))
        return errors
