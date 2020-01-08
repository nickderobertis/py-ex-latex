from typing import Union, TYPE_CHECKING
from pyexlatex.models.item import MultiOptionSimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.texgen import _multi_option_item_str
if TYPE_CHECKING:
    from pyexlatex.models.format.text.color.deftypes.base import ColorDefinition


class TextColor(TextAreaMixin, MultiOptionSimpleItem):
    """
    Changes the color of text.

    Usage:
    >>> import pyexlatex as pl
    >>> pl.TextColor('something', pl.Hex('59bf37'))
    >>> pl.TextColor('something', pl.RGB(89, 191, 55))
    >>> pl.TextColor('something', 'blue', opacity=0.5)
    """
    name = 'textcolor'

    def __init__(self, content, color: Union[str, 'ColorDefinition'], opacity: float = 1.0, **kwargs):
        """

        :param content:
        :param color: can pass a string name of an existing color, such as 'green' or 'red', or can pass a defined
            color, using one of the ColorDefinition models, e.g. RGB or Hex
        :param opacity:
        :param kwargs:
        """
        self.opacity = opacity
        self.init_data()
        self.data.packages.append('xcolor')
        self.color = self.process_color_get_name(color)
        self.content = content
        contents = self.format_contents(content)
        MultiOptionSimpleItem.__init__(self, self.name, self.color_str, contents, **kwargs)

    @property
    def opacity_str(self) -> str:
        if self.opacity != 1:
            return f'!{self.opacity * 100:.0f}'

        return ''

    @property
    def color_str(self) -> str:
        return f'{self.color}{self.opacity_str}'

    def process_color_get_name(self, color: Union[str, 'ColorDefinition']) -> str:
        if isinstance(color, str):
            return color

        # Got color definition. Need to add to preamble and reference by the name of the color
        self.data.packages.append(color)
        return color.color_name

    def __str__(self):
        return _multi_option_item_str(self.name, self.color_str, self.content, overlay=self.overlay)