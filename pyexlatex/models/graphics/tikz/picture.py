from typing import Optional, Sequence
from dero.latex.models.item import Item
from dero.latex.models.section.base import TextAreaMixin
from dero.latex.models.package import Package


class TikZPicture(TextAreaMixin, Item):
    name = 'tikzpicture'

    def __init__(self, contents, env_modifiers: Optional[Sequence[str]]=None):
        self.init_data()
        self.data.packages.append(Package('tikz'))
        super().__init__(self.name, contents, env_modifiers=env_modifiers)

