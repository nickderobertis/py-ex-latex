from typing import List, Union
import posixpath
import os

from pyexlatex.texgen import _include_graphics_str
from pyexlatex.models.item import ItemBase
from pyexlatex.models.sizes.linewidth import LineWidth


class Graphic(ItemBase):

    def __init__(self, filepath, width: Union[str, float] = 1.0, cache: bool = True):
        """

        Args:
            filepath:
            width: if a float is passed, is interpreted as a fraction of line width. if a str is passed, will be passed
                into latex directly
            cache:
        """
        self._set_path(filepath)
        self.width = width
        self.binaries = None

        if cache:
            self._cache(filepath)

    def __repr__(self):
        return f'<Graphic({self.filepaths[0]}, width={self.width})>'

    def __str__(self):
        return _include_graphics_str(self.source_paths[0], self.width_str)

    def _set_path(self, filepath: str):
        from pyexlatex.texgen.replacements.filename import _latex_valid_basename

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

    @property
    def width_str(self) -> str:
        # Handle float being passed
        if isinstance(self.width, (float, int)):
            return f'{self.width}{LineWidth()}'

        # Handle manually passing a width string
        return self.width
