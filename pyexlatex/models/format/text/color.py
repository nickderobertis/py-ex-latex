from pyexlatex.texgen import _multi_option_item_str
from pyexlatex.models.item import MultiOptionSimpleItem
from pyexlatex.models.package import Package
from pyexlatex.models.section.base import TextAreaMixin

class TextColor(TextAreaMixin, MultiOptionSimpleItem):
    """
    Changes the color of text.
    """
    name = 'textcolor'

    def __init__(self, content, color: str, opacity: float = 1.0, **kwargs):
        self.color = color
        self.opacity = opacity
        self.init_data()
        self.data.packages.append(Package('xcolor'))
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

    def __str__(self):
        return _multi_option_item_str(self.name, self.color_str, self.content, overlay=self.overlay)
