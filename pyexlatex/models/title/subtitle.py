from pyexlatex.models.item import SimpleItem


class Subtitle(SimpleItem):
    name = 'subtitle'

    def __init__(self, subtitle: str):
        self.subtitle = subtitle
        super().__init__(self.name, self.subtitle)