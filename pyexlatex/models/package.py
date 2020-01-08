from pyexlatex.texgen import _usepackage_str
from pyexlatex.models.item import ItemBase


class Package(ItemBase):
    r"""
    Represents LaTeX \usepackage{}, pass to Document if any custom LaTeX packages are needed.
    """
    equal_attrs = ['name', 'modifier_str']

    def __init__(self, name, modifier_str=None):
        self.name = name
        self.modifier_str = modifier_str

    def __repr__(self):
        return f'<Package(name={self.name})>'

    def __str__(self):
        return _usepackage_str(self.name, self.modifier_str)

    def matches_name(self, other):
        return self.name == other

