from pyexlatex.models.item import MultiOptionSimpleItem
from pyexlatex.models.package import Package

class TextColor(MultiOptionSimpleItem):
    name = 'textcolor'

    def __init__(self, content, color: str, opacity: float = 1.0, **kwargs):
        self.color = color
        self.opacity = opacity
        self.init_data()
        self.data.packages.append(Package('xcolor'))
        super().__init__(self.name, self.color_str, content, **kwargs)

    @property
    def opacity_str(self) -> str:
        if self.opacity != 1:
            return f'!{self.opacity * 100:.0f}'

        return ''

    @property
    def color_str(self) -> str:
        return f'{self.color}{self.opacity_str}'
