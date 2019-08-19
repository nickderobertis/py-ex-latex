from typing import Sequence
from pyexlatex.models.item import Item
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.package import Package


class AdjustBox(TextAreaMixin, Item):
    name = 'adjustbox'

    def __init__(self, contents, adjust_options: Sequence[str]):
        self.adjust_options = adjust_options
        self.init_data()
        self.data.packages.append(Package('adjustbox'))
        super().__init__(self.name, contents, env_modifiers=self.options_str)

    @property
    def options_str(self) -> str:
        base_str = ', '.join(self.adjust_options)
        return self._wrap_with_braces(base_str)

