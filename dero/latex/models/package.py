from dero.latex.texgen import _usepackage_str


class Package:

    def __init__(self, name, modifier_str=None):
        self.name = name
        self.modifier_str = modifier_str

    def __repr__(self):
        return f'<Package(name={self.name})>'

    def __str__(self):
        return _usepackage_str(self.name, self.modifier_str)

    def __eq__(self, other):
        return (self.name == other.name) and (self.modifier_str == other.modifier_str)

    def __hash__(self):
        return hash((self.name, self.modifier_str))

    def matches_name(self, other):
        return self.name == other

