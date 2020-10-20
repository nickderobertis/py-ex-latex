import re
from typing import List

from mixins.repr import ReprMixin
from pyexlatex.models.item import ItemBase
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.texgen.packages.columntypes import ColumnTypesPackage


class ColumnAlignment(ReprMixin, ItemBase):
    """
    Alignment of a single column in a table
    """
    repr_cols = ['align']

    def __init__(self, align_str: str):
        self._validate_align_str(align_str)
        self.align = align_str

    def __str__(self):
        return self.align

    def __add__(self, other):
        return self.align + other.align

    def __radd__(self, other):
        return other.align + self.align

    def _validate_align_str(self, align_str):
        basic_pattern = re.compile(r'[lcr|.]')
        length_pattern = re.compile(r'[LCR]\{[\d\w\s.]+\}')

        basic_match = basic_pattern.fullmatch(align_str)
        length_match = length_pattern.fullmatch(align_str)

        if length_match:
            self._add_requirements_for_length_match()

        if not (basic_match or length_match):
            raise ValueError(f'expected alignment of l, c, r, ., |, L{{size}}, C{{size}}, or R{{size}}. Got {align_str}')

    def _add_requirements_for_length_match(self):
        self.add_package(ColumnTypesPackage())


class ColumnsAlignment(ReprMixin, ContainerItem):
    """
    A set of column alignments, usually for the whole table
    """
    repr_cols = ['aligns']

    def __init__(self, aligns: List[ColumnAlignment] = None, num_columns: int=None):
        self.aligns = ColumnsAlignment._get_aligns(aligns, num_columns)
        self.add_data_from_content(self.aligns)

    def __str__(self):
        return ''.join(str(align) for align in self.aligns)

    def __iter__(self):
        for align in self.aligns:
            yield align

    @staticmethod
    def _get_aligns(aligns: List[ColumnAlignment] = None, num_columns: int=None):
        if aligns is None and num_columns is None:
            raise ValueError('must pass aligns or num columns')

        # default align is first column left, rest centered
        if aligns is None and num_columns is not None:
            return [ColumnAlignment('l')] + [ColumnAlignment('c')] * (num_columns - 1)

        # if we don't know how many columns, must assume passed number of aligns is correct
        if num_columns is None:
            return aligns

        # Shouldn't hit this block, but needed for typing
        if aligns is None:
            raise ValueError('must pass aligns or num columns')

        # number of alignments matches number of columns. no extra processing needed
        if len(aligns) == num_columns:
            return aligns

        # if one alignment is passed with many columns, use that align with all columns
        if len(aligns) == 1:
            return [aligns[0]] * num_columns
        else:
            raise ValueError(f'got {len(aligns)} alignments for {num_columns} columns. unclear how to apply')

    @classmethod
    def from_alignment_str(cls, align_str: str, num_columns: int=None):
        align_str_list = _full_align_str_to_align_str_list(align_str)
        aligns = [ColumnAlignment(align) for align in align_str_list]

        return cls(aligns, num_columns=num_columns)


def _full_align_str_to_align_str_list(align_str: str):
    split_letters = ['l', 'c', 'r', '|', 'L', 'C', 'R', '.']
    out_list = []
    collected_letters = ''
    split = True

    for letter in align_str:
        # beginning inside of length str. don't split while inside
        if letter == '{':
            split = False
        # end of inside of length str. turn splitting back on
        if letter == '}':
            split = True
        # if splitting, output what we've got so far and start a new item
        if split and letter in split_letters:
            out_list.append(collected_letters)
            collected_letters = ''
        # if not splitting, add to current item
        collected_letters += letter

    # Clean up list from loop. Remove first (always blank), and add last
    out_list.append(collected_letters)
    out_list = out_list[1:]

    return out_list