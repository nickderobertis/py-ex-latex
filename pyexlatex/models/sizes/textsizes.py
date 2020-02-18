from pyexlatex.models.item import NoOptionsNoContentsItem

LATEX_SIZES = [
    'tiny',
    'scriptsize',
    'footnotesize',
    'small',
    'normalsize',
    'large',
    'Large',
    'LARGE',
    'huge',
    'Huge'
]

class TextSize(NoOptionsNoContentsItem):
    """
    Resize text in this group by a relative size.
    """

    def __init__(self, relative_size_int: int):
        """
        :param relative_size_int: 0 gets the normal font size, negative numbers get smaller sizes, positive numbers get
            larger sizes. Range is from -4 to 5
        """

        self.relative_size_int = relative_size_int
        self._validate()
        self.name = latex_size_str_for_relative_size_int(self.relative_size_int)
        super().__init__(self.name)


    def _validate(self):
        if self.relative_size_int < -4 or self.relative_size_int > 5:
            raise ValueError('relative size int must be in the range of -4 to 5')


def latex_size_str_for_relative_size_int(relative_size_int: int) -> str:
    latex_size_index = relative_size_int + 4
    return LATEX_SIZES[latex_size_index]
