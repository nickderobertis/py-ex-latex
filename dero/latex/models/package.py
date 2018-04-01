from dero.latex.texgen import _usepackage_str


class Package:

    def __init__(self, name, modifier_str=None):
        self.name = name
        self.modifier_str = modifier_str

    def __repr__(self):
        return f'<Package(name={self.name})>'

    def __str__(self):
        return _usepackage_str(self.name, self.modifier_str)

