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
    if num_values_to_add < 0:
        return _negative_pad_obj(obj, abs(num_values_to_add), direction=direction)

    if direction == 'right':
        obj.values += [CellSpacer(num_values_to_add)]
    elif direction == 'left':
        obj.values = [CellSpacer(num_values_to_add)] + obj.values
    else:
        raise ValueError(f'must pass left or right for direction. got {direction}')


def _negative_pad_obj(obj, num_values_to_remove: int, direction='right'):
    """
    Used in the case where row has too many values. If any of those
    values are spacers in the same direction, remove as many as are
    needed. If they are not spacers or too many need to be removed,
    raises an error.
    """
    num_existing_spacers = _get_length_of_spacers_in_direction(obj, direction)
    if num_existing_spacers < num_values_to_remove:
        raise ValueError(f'not able to adjust row {obj} to remove {num_values_to_remove} spacers')
    _remove_spacers_in_direction(obj, direction=direction)
    num_values_to_add = num_existing_spacers - num_values_to_remove

    if num_values_to_add == 0:
        return

    if direction == 'right':
        obj.values += [CellSpacer(num_values_to_add)]
    elif direction == 'left':
        obj.values = [CellSpacer(num_values_to_add)] + obj.values
    else:
        raise ValueError(f'must pass left or right for direction. got {direction}')


def _get_length_of_spacers_in_direction(obj, direction='right') -> int:
    if direction == 'right':
        values = reversed(obj.values)
    elif direction == 'left':
        values = obj.values
    else:
        raise ValueError(f'must pass left or right for direction. got {direction}')

    spacer_length = 0
    for value in values:
        if isinstance(value, CellSpacer):
            spacer_length += value.span
        else:
            break
    return spacer_length


def _remove_spacers_in_direction(obj, direction='right'):
    if direction == 'right':
        last_spacer_idx = -1
        for i, value in enumerate(reversed(obj.values)):
            if not isinstance(value, CellSpacer):
                last_spacer_idx = -i
                break
        obj.values = obj.values[:last_spacer_idx]
    elif direction == 'left':
        last_spacer_idx = 0
        for i, value in enumerate(obj.values):
            if not isinstance(value, CellSpacer):
                last_spacer_idx = i - 1
                break
        obj.values = obj.values[last_spacer_idx + 1:]
    else:
        raise ValueError(f'must pass left or right for direction. got {direction}')
