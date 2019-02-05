from typing import Union
from sympy import Eq, latex
from dero.latex.models.item import IsLatexItemMixin
from dero.latex.models.mixins import IsSpecificClassMixin
from dero.latex.logic.format import eq as format_eq

class Equation(IsSpecificClassMixin, IsLatexItemMixin):
    name = 'equation'

    def __init__(self, eq: Union[Eq, str], inline: bool = True):
        self.formatted_eq = self.format_eq(eq, inline=inline)
        super().__init__()

    def __str__(self):
        return self.formatted_eq

    @staticmethod
    def format_eq(eq: Union[Eq, str], inline: bool = True):
        if isinstance(eq, str):
            # already formatted
            return eq

        if inline:
            return format_eq.inline(eq)
        else:
            return format_eq.offset(eq)

