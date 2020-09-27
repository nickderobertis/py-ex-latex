from typing import Dict, Sequence, Optional

from pyexlatex.models.sizes.textsizes import TextSize
from pyexlatex.models.item import SimpleItem


class CaptionSetup(SimpleItem):
    """
    Control formatting of captions for tables and figures
    """
    name = 'captionsetup'

    def __init__(self, target: str = 'figure', relative_sizes: Optional[Dict[str, int]] = None,
                 options: Optional[Sequence[str]] = None):
        self.init_data()
        self.add_package('caption')

        if relative_sizes is None:
            relative_sizes = {}

        if options is None:
            options = []
        else:
            options = list(options)

        size_options = {name: TextSize(size).name for name, size in relative_sizes.items()}
        size_options_str = SimpleItem._dict_to_options_str(size_options)
        options_str = ','.join([*options, size_options_str])

        target_str = self._wrap_with_bracket(target)

        super().__init__(self.name, options_str, pre_modifiers=target_str)
