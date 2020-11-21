from typing import Iterable, Sequence

from mixins.repr import ReprMixin
from pyexlatex.table.models.data.dataitem import DataItem
from pyexlatex.table.models.labels.label import Label
from pyexlatex.table.models.mixins.addvalues.row import RowAddMixin
from pyexlatex.table.models.spacing.cell import CellSpacer


class RowBase(ReprMixin, RowAddMixin):
    values: Sequence

    def __len__(self):
        return sum(_get_length(value) for value in self.values)

    def __iter__(self):
        for value in self.values:
            yield value

    def __getitem__(self, item):
        return self.values[item]

    def __eq__(self, other):
        if not hasattr(other, 'values'):
            return False
        if len(self.values) != len(other.values):
            return False

        for val, other_value in zip(self.values, other.values):
            if val != other_value:
                return False

        return True

    def pad(self, length: int, direction='right'):
        """
        Expand row out to the right or left with blanks, until it is length passed
        :param length:
        :return:
        """
        _pad_obj(self, length=length, direction=direction)

    @property
    def is_spacer(self):
        booleans = []
        for item in self.values:
            if isinstance(item, CellSpacer):
                result = True
            elif isinstance(item, (Label, DataItem)):
                result = str(item.value).strip() == ''
            elif isinstance(item, str):
                result = item.strip() == ''
            else:
                raise ValueError(f'cannot check whether {item} of type {type(item)} is a spacer or not')
            booleans.append(result)
        return all(booleans)


def _get_length(obj):
    from pyexlatex.table.models.texgen.lines import TableLineOfSegments, TableLineSegment
    from pyexlatex.table.models.labels.collection import LabelCollection
    if isinstance(obj, (Label, LabelCollection, DataItem, TableLineOfSegments, TableLineSegment)):
        return len(obj)
    else:
        return 1

def _pad_obj(obj, length: int, direction='right'):
    """
    Expand row out to the right or left with blanks, until it is length passed
    :param length:
    :return:
    """
    num_values_to_add = length - len(obj)
    direction = direction.lower().strip()

    if num_values_to_add == 0:
        return

    if direction == 'right':
        obj.values += [CellSpacer(num_values_to_add)]
    elif direction == 'left':
        obj.values = [CellSpacer(num_values_to_add)] + obj.values
    else:
        raise ValueError(f'must pass left or right for direction. got {direction}')