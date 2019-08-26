from typing import Optional, Sequence
from pyexlatex.models.item import Item
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.models.package import Package


class TikZPicture(TextAreaMixin, Item):
    """
    Container which holds any graphics.
    """
    name = 'tikzpicture'

    def __init__(self, contents, env_modifiers: Optional[Sequence[str]]=None):
        self.init_data()
        self.data.packages.append(Package('tikz'))
        super().__init__(self.name, contents, env_modifiers=env_modifiers)

