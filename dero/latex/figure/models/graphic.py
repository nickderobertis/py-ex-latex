from typing import List
import posixpath
import os

from dero.latex.models.mixins import StringAdditionMixin
from dero.latex.texgen import _include_graphics_str
from dero.latex.models.item import ItemBase


class Graphic(ItemBase):

    def __init__(self, filepath, width=r'\linewidth', cache: bool = True):
        self._set_path(filepath)
        self.width = width
        self.binaries = None

        if cache:
            self._cache(filepath)

    def __repr__(self):
        return f'<Graphic({self.filepaths[0]}, width={self.width})>'

    def __str__(self):
        return _include_graphics_str(self.source_paths[0], self.width)

    def _set_path(self, filepath: str):
        from dero.latex.texgen.replacements.filename import _latex_valid_basename

        basename = _latex_valid_basename(filepath)
        source_path = posixpath.join('Sources', basename)

        self._filepath_parts = filepath.split(os.path.sep)
        self.source_paths = [source_path]

    def _cache(self, filepath: str):
        with open(filepath, 'rb') as f:
            self.binaries = [f.read()]

    @property
    def filepaths(self) -> List[str]:
        return [os.path.sep.join(self._filepath_parts)]

