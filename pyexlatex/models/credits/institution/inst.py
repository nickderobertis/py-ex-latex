from typing import Optional
from pyexlatex.models.item import SimpleItem


class Inst(SimpleItem):
    name = 'inst'

    def __init__(self, num: int):
        self.num = num
        super().__init__(self.name, str(num))