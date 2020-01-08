from pyexlatex.models.item import Item
from pyexlatex.models.package import Package
from pyexlatex.constants.flags import HAS_MINTED


class Minted(Item):
    name = 'minted'

    def __init__(self, content, language: str):
        self.init_data()
        self.data.packages.append(Package('minted'))
        self.data.flags.append(HAS_MINTED)
        super().__init__(self.name, content, env_modifiers=self._wrap_with_braces(language))
