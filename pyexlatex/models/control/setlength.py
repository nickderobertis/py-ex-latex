from pyexlatex.models.item import MultiOptionSimpleItem


class SetLength(MultiOptionSimpleItem):
    name = 'setlength'

    def __init__(self, set_for: str, value: str):
        self.set_for = set_for
        self.value = value

        super().__init__(self.name, set_for, value)
