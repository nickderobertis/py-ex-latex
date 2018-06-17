import posixpath

from dero.latex.models.mixins import StringAdditionMixin
from dero.latex.texgen import _include_graphics_str


class Graphic(StringAdditionMixin):

    def __init__(self, filepath, width=r'\linewidth'):
        self._set_path(filepath)
        self.width = width

    def __repr__(self):
        return f'<Graphic({self.filepath}, width={self.width})>'

    def __str__(self):
        return _include_graphics_str(self.source_path, self.width)

    def _set_path(self, filepath: str):
        from dero.latex.logic.pdf import _latex_valid_basename

        basename = _latex_valid_basename(filepath)
        source_path = posixpath.join('Sources', basename)

        self.filepath = filepath
        self.source_path = source_path


