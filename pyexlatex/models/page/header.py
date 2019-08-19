from dero.latex.models.item import SimpleItem
from dero.latex.logic.builder import _build

class FancyHeader(SimpleItem):
    name = 'fancyhead'

    def __init__(self, contents):
        super().__init__(self.name, contents)

remove_header_line = r'\renewcommand{\headrulewidth}{0pt}'
remove_header = _build([
    remove_header_line,
    FancyHeader('')  # remove header default contents
])