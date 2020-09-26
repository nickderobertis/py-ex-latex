from typing import Union, Sequence

from pyexlatex.models.commands.renewcommand import ReNewCommand
from pyexlatex.models.item import SimpleItem


class RightFooter(SimpleItem):
    """
    A right-aligned footer
    """
    name = 'rfoot'

    def __init__(self, contents):
        super().__init__(self.name, contents)


class CenterFooter(SimpleItem):
    """
    A center-aligned footer
    """
    name = 'cfoot'

    def __init__(self, contents):
        super().__init__(self.name, contents)


class LeftFooter(SimpleItem):
    """
    A left-aligned footer
    """
    name = 'lfoot'

    def __init__(self, contents):
        super().__init__(self.name, contents)


class FooterLine(ReNewCommand):
    """
    Add a horizontal line above the footer
    """

    def __init__(self, size: float = 0.4, units: str = 'pt'):
        size_str = f'{size}{units}'
        super().__init__(r'footrulewidth', size_str)


FooterType = Union[RightFooter, LeftFooter, CenterFooter, FooterLine]
Footers = Sequence[FooterType]
