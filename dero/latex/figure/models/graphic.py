from dero.latex.models.mixins import StringAdditionMixin
from dero.latex.texgen import _include_graphics_str


class Graphic(StringAdditionMixin):

    def __init__(self, filepath, width=r'\linewidth'):
        self.filepath = filepath
        self.width = width

    def __repr__(self):
        return f'<Graphic({self.filepath}, width={self.width})>'

    def __str__(self):
        return _include_graphics_str(self.filepath, self.width)


