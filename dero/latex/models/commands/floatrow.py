from dero.latex.models.item import MultiOptionSimpleItem, SimpleItem
from dero.latex.models.sizes.textsizes import Size

class DeclareFloatFont(MultiOptionSimpleItem):
    name = 'DeclareFloatFont'

    def __init__(self, relative_size_int: int):
        self.size_def = Size(relative_size_int)
        super().__init__(self.name, self.size_def.name, self.size_def)


class FloatSetup(SimpleItem):
    name = 'floatsetup'

    def __init__(self, targeted_float: str, options: str):
        super().__init__(self.name, options, pre_modifiers=f'[{targeted_float}]')
