from pyexlatex.models.item import MultiOptionSimpleItem
from pyexlatex.models.format.noindent import NoIndent


class Rule(MultiOptionSimpleItem):
    """
    Draw a horizontal line of given length and thickness
    """
    name = 'rule'

    def __init__(self, length: float = 2, thickness: float = 0.4):
        self.length = length
        self.thickness = thickness
        super().__init__(self.name, self.length_str, self.thickness_str)

    def __str__(self):
        contents = super().__str__()
        all_contents = NoIndent(contents)
        return str(all_contents)

    @property
    def length_str(self):
        if isinstance(self.length, float):
            return f'{self.length}cm'
        return self.length

    @property
    def thickness_str(self):
        if isinstance(self.thickness, float):
            return f'{self.thickness}pt'
        return self.thickness
