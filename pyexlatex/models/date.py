from pyexlatex.models.item import SimpleItem
from pyexlatex.texgen import _todays_date_str

class Date(SimpleItem):
    name = 'date'

    def __init__(self, contents=None):
        if contents is None:
            contents = _todays_date_str()
        super().__init__(self.name, contents)