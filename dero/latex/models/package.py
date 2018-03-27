
class Package:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Package(name={self.name})>'

    def __str__(self):
        return _usepackage_str(self.name)

def _usepackage_str(str_):
    return rf'\usepackage{{{str_}}}'