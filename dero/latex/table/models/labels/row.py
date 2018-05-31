from dero.latex.table.models.table.row import Row
from dero.latex.table.models.labels.collection import LabelCollection
from dero.latex.table.models.labels.multicolumn import MultiColumn

class LabelRow(Row):

    def __init__(self, values: LabelCollection, length: int=None):
        self.length = length if length is not None else len(values)
        super().__init__(values)

    def __str__(self):
        num_values = len(self.values)
        # as many columns as values, simply sum
        if self.length == num_values:
            return sum(self.values)
        # from here, passed length different than length of values
        # if only one value, use multicolumn format over number of columns
        elif num_values == 1:
            return MultiColumn(contents=self.values[0], span=self.length)
        # differing number of values from length, but number of values is not 1
        # therefore it is unclear how to expand into a multicolumn format
        # (how many columns should each label span?)
        else:
            raise NotImplementedError('got different length of label row from number of labels, and number of '
                                      f'labels was not 1. got {num_values} labels to cover {self.length} columns')