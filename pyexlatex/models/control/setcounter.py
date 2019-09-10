from pyexlatex.models.item import MultiOptionSimpleItem


class SetCounter(MultiOptionSimpleItem):
    name = 'setcounter'

    def __init__(self, set_for: str, value: int):
        self.set_for = set_for
        self.value = value

        super().__init__(self.name, set_for, str(value))
