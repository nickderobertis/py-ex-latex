import posixpath
import os

from dero.latex.models.mixins import StringAdditionMixin
from dero.latex.texgen import _include_graphics_str


class Graphic(StringAdditionMixin):

    def __init__(self, filepath, width=r'\linewidth', cache: bool = True):
        self._set_path(filepath)
        self.width = width
        self.binary = None

        if cache:
            self._cache(filepath)

    def __repr__(self):
        return f'<Graphic({self.filepath}, width={self.width})>'

    def __str__(self):
        return _include_graphics_str(self.source_path, self.width)

    def _set_path(self, filepath: str):
        from dero.latex.texgen.replacements.filename import _latex_valid_basename

        basename = _latex_valid_basename(filepath)
        source_path = posixpath.join('Sources', basename)

        self._filepath_parts = filepath.split(os.path.sep)
        self.source_path = source_path

    def _cache(self, filepath: str):
        with open(filepath, 'rb') as f:
            self.binary = f.read()

    @property
    def filepath(self):
        return os.path.sep.join(self._filepath_parts)

