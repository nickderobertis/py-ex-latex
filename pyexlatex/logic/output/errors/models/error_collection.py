from typing import List, Dict, Union
import warnings
from latex.exc import LatexBuildError
from pyexlatex.logic.output.errors.models.error import LatexError


class LatexErrorCollection:

    def __init__(self, latex_build_error: LatexBuildError):
        self.exc = latex_build_error
        self.errors = self._parse_errors()

    def __getitem__(self, index):
        return self.errors[index]

    def __iter__(self):
        return iter(self.errors)

    def _parse_errors(self) -> List[LatexError]:
        error_dict_list = get_errors_dict_list(self.exc)
        errors = []
        for error_dict in error_dict_list:
            arg_dict = error_dict.copy()
            arg_dict.pop('error')
            errors.append(LatexError(**arg_dict))  # type: ignore
        if not errors:
            warnings.warn(f'got LatexBuildError with no errors attached: {self.exc}')
        return errors

def get_errors_dict_list(exc: LatexBuildError) -> List[Dict[str, Union[str, int, List[str]]]]:
    try:
        return exc.get_errors()
    except AttributeError as e:
        if "'NoneType' object has no attribute 'splitlines'" in str(e):
            return []
        raise e