from pyexlatex.models.item import Item
from pyexlatex.models.package import Package


class Minted(Item):
    name = 'minted'

    def __init__(self, content, language: str):
        self.init_data()
        self.data.packages.append(Package('minted'))
        super().__init__(self.name, content, env_modifiers=self._wrap_with_braces(language))
