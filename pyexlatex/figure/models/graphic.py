from typing import List, Union, Sequence, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay
import posixpath
import os

from pyexlatex.models.item import SimpleItem
from pyexlatex.models.sizes.textwidth import TextWidth


class Graphic(SimpleItem):
    """
    Basic class for including graphics, just the image with no structure.

    In most documents, a Figure would be used to give more structure to the graphic. This class will literally just
    include the image with no other structure. It is typically more useful in presentations where the structure
    is already being provided.
    """
    name = 'includegraphics'

    def __init__(self, filepath: str, width: Union[str, float] = 1.0, cache: bool = True, options: List[str] = None,
                 overlay: Optional['Overlay'] = None):
        """

        :param filepath:
        :param width: if a float is passed, is interpreted as a fraction of line width. if a str is passed, will be passed
            into latex directly
        :param cache:
        :param options:
        :param overlay: beamer overlay
        """
        self._set_path(filepath)
        self.width = width
        self.binaries = None

        self.options = self._get_list_copy_from_list_or_none(options)
        self.options.append(
            f'width={self.width_str}'
        )

        if cache:
            self._cache(filepath)

        super().__init__(
            self.name,
            self.source_paths[0],
            pre_modifiers=self.options_str,
            overlay=overlay,
            format_content=False
        )

    def __repr__(self):
        return f'<Graphic({self.filepath}, width={self.width})>'

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
    def filepath(self) -> str:
        return self.filepaths[0]

    @property
    def source_path(self) -> str:
        return self.source_paths[0]

    @property
    def width_str(self) -> str:
        # Handle float being passed
        if isinstance(self.width, (float, int)):
            return f'{self.width}{TextWidth()}'

        # Handle manually passing a width string
        return self.width

    @property
    def options_str(self) -> Optional[str]:
        if self.options is None:
            return None

        return self._wrap_with_bracket(', '.join(self.options))
