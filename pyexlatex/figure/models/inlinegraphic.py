from typing import Union, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pyexlatex.presentation.beamer.overlay.overlay import Overlay

from pyexlatex.models.item import SimpleItem, MultiOptionSimpleItem
from pyexlatex.figure.models.graphic import Graphic
from pyexlatex.models.format.raw import Raw


class InlineGraphic(MultiOptionSimpleItem, Graphic):
    """
    A version of Graphic that is meant to be used within text. It centers the text vertically
    when the graphic is taller than the text.
    """
    name = 'vcenteredinclude'
    options: tuple  # type: ignore

    def __init__(self, filepath, width: Union[str, float] = 1.0, cache: bool = True,
                 options: Optional[List[str]] = None,
                 overlay: Optional['Overlay'] = None):
        self.init_data()
        self.add_package('graphicx')
        self.data.packages.append(self._command_definition)

        self._set_path(filepath)
        self.width = width
        self.binaries = None

        self.options_list = self._get_list_copy_from_list_or_none(options)
        self.options_list.append(
            f'width={self.width_str}'
        )

        if cache:
            self._cache(filepath)

        options_str = ','.join(self.options_list)
        self.options = (options_str, self.source_paths[0])
        self.overlay = overlay

    @property
    def _command_definition(self) -> Raw:
        # TODO [#41]: set inline graphic command definition using models
        return Raw(
r"""
\newcommand{\vcenteredinclude}[2]{\begingroup
\setbox0=\hbox{\includegraphics[#1]{#2}}%
\parbox{\wd0}{\box0}\endgroup}
""".strip()
        )