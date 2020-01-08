from typing import Optional, Any
from pyexlatex.models.item import ItemBase
from pyexlatex.texgen import no_options_no_contents_str
from mixins.repr import ReprMixin

class Mode(ItemBase, ReprMixin):
    name = 'mode'
    repr_cols = [
        'mode_type',
        'contents'
    ]

    def __init__(self, mode_type: str = 'presentation', contents: Optional[Any] = None):
        self.mode_type = mode_type
        self.contents = contents
        super().__init__()

    def __str__(self):
        """
        \mode must be on its own line with no whitespace in some cases, so must have a custom __str__ method
        """
        from pyexlatex.logic.builder import _build
        from pyexlatex.logic.format.contents import format_contents
        mode_definition = no_options_no_contents_str(self.name)  # \mode
        mode_type_str = f'<{self.mode_type}>'
        contents_str = f'{{{format_contents(self.contents)}}}'
        mode_contents = f'{mode_type_str}{contents_str}'
        return _build([
            mode_definition,
            mode_contents
        ])

