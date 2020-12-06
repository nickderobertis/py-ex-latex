from typing import Union, Optional
from sympy import Eq

from pyexlatex.models.item import IsLatexItemMixin
from pyexlatex.models.mixins import IsSpecificClassMixin
from pyexlatex.logic.format import eq as format_eq

class Equation(IsSpecificClassMixin, IsLatexItemMixin):
    """
    Pass sympy or string equations to have them rendered in LaTeX.
    """
    name = 'equation'

    def __init__(self, eq: Optional[Eq] = None, str_eq: Optional[str] = None,
                 inline: bool = True, numbered: bool = True):
        self._validate(eq, str_eq)
        self.eq_str = eq if eq is not None else str_eq
        self.inline = inline
        self.numbered = numbered
        super().__init__()

    def __str__(self):
        return self.formatted_eq

    @property
    def formatted_eq(self):
        if self.inline:
            return format_eq.inline(self.eq_str)
        elif self.numbered:
            return format_eq.offset(self.eq_str)
        else:
            return format_eq.offset_no_numbering(self.eq_str)

    def _validate(self, eq: Optional[Eq] = None, str_eq: Optional[str] = None):
        if eq is None and str_eq is None:
            raise ValueError('must pass one of eq or str_eq')
        if eq is not None and str_eq is not None:
            raise ValueError('must pass at most one of eq or str_eq')

    @property
    def eq_str(self):
        return self._eq_str

    @eq_str.setter
    def eq_str(self, value: Union[Eq, str]):
        if isinstance(value, str):
            # already formatted
            self._eq_str = value
        else:
            from sympy import latex
            self._eq_str = latex(value)
