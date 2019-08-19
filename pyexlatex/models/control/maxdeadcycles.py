from pyexlatex.models.item import EqualsItem

class MaxDeadCycles(EqualsItem):
    name = 'maxdeadcycles'

    def __init__(self, num_cycles: int = 200):
        super().__init__(self.name, str(num_cycles))
