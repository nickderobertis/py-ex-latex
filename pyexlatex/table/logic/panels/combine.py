import copy
from typing import List, Sequence

from pyexlatex.table.models.panels.grid import GridShape
from pyexlatex.table.models.labels.table import LabelTable
from pyexlatex.table.models.labels.collection import LabelCollection
from pyexlatex.table.models.table.section import TableSection

def common_column_labels(grid: GridShape, use_object_equality=True, enforce_label_order=True):
    axis = 1 # columns
    all_column_ints = list(range(grid.shape[1]))

    return _selected_common_labels_for_axis(
        grid,
        selections=all_column_ints,
        axis=axis,
        use_object_equality=use_object_equality,
        enforce_label_order=enforce_label_order
    )

def common_row_labels(grid: GridShape, use_object_equality=True, enforce_label_order=True):
    axis = 0  # rows
    all_row_ints = list(range(grid.shape[0]))

    return _selected_common_labels_for_axis(
        grid,
        selections=all_row_ints,
        axis=axis,
        use_object_equality=use_object_equality,
        enforce_label_order=enforce_label_order
    )


def _selected_common_labels_for_axis(grid: GridShape, selections: Sequence[int]=(0,), axis: int=0, use_object_equality=True,
                                     enforce_label_order=True):
    common_label_tables: List[LabelTable] = []
    for i in selections:
        common_label_tables.append(
            _common_labels(
                grid,
                i,
                axis=axis,
                use_object_equality=use_object_equality,
                enforce_label_order=enforce_label_order
            )
        )

    non_none_tables = [table for table in common_label_tables if table is not None]

    if non_none_tables == []:
        return None

    return non_none_tables


def _common_labels(grid: GridShape, num: int, axis: int=0, use_object_equality=True,
                   enforce_label_order=True):
    subgrid = _get_subgrid(
        grid=grid,
        num=num,
        axis=axis
    )

    label_attr = _get_label_attr(axis=axis)

    label_tables: List[LabelTable] = [getattr(section, label_attr, None) for section in subgrid]

    # first labels missing, no consolidation to be done, consolidated labels are None
    if label_tables[0] is None:
        return None

    common_label_table = LabelTable([])
    for i, label_collection in enumerate(label_tables[0]):
        stored_match = False # only want to add each matched collection once. use boolean to track
        for label_table in label_tables[1:]:
            # If there is a corresponding label table and it has this index label collection
            if label_table is not None and i < len(label_table.label_collections):
                match = _compare_label_collections(
                    label_collection,
                    label_table[i],
                    use_object_equality=use_object_equality
                )
            else:
                # No labels, nothing to consolidate
                match = False
            if match:
                if not stored_match:
                    common_label_table.append(label_collection)
                    stored_match = True
            else:
                if enforce_label_order:
                    break # as soon as one label collection doesn't match, stop consolidating
                else:
                    continue # don't worry about non-match, continue consolidating

    if common_label_table.is_empty:
        return None

    return common_label_table

def remove_label_collections_from_grid(grid: GridShape, column_labels: List[LabelTable] = None,
                                       row_labels: List[LabelTable] = None, use_object_equality=True):
    for row in grid:
        for section in row:
            if column_labels is not None:
                for label_table in column_labels:
                    _remove_label_collections(
                        section,
                        label_table,
                        axis=1,
                        use_object_equality=use_object_equality,
                        inplace=True
                    )
            if row_labels is not None:
                for label_table in row_labels:
                    _remove_label_collections(
                        section,
                        label_table,
                        axis=0,
                        use_object_equality=use_object_equality,
                        inplace=True
                    )

def _remove_label_collections(section: TableSection, label_table: LabelTable, axis: int=0,
                              use_object_equality=True, inplace=False):

    # Handle section not having labels for this axis
    label_attr = _get_label_attr(axis=axis)
    if not hasattr(section, label_attr):
        return section

    # Now has labels for this axis. Create a copy to avoid modifying original
    if not inplace:
        section = copy.deepcopy(section)

    for label_collection in label_table:
        section_label_table: LabelTable = getattr(section, label_attr, [])
        if section_label_table is not None:
            for section_label_collection in section_label_table:
                match = _compare_label_collections(
                    label_collection,
                    section_label_collection,
                    use_object_equality=use_object_equality
                )
                if match:
                    section_label_table.remove(section_label_collection)


    # once all label collections have been removed, remove table
    section_label_table = getattr(section, label_attr, False)
    if section_label_table and section_label_table.label_collections == []:
        setattr(section, label_attr, None)

    return section


def _get_label_attr(axis: int=0):
    # select rows
    if axis == 0:
        return 'row_labels'
    # select columns
    elif axis == 1:
        return 'column_labels'
    else:
        raise ValueError(f'axis must be 0 or 1, got {axis}')

def _get_subgrid(grid: GridShape, num: int, axis: int=0):
    # select rows
    if axis == 0:
        return _grid_if_not(grid[num])
    # select columns
    elif axis == 1:
        return _grid_if_not(grid[:, num])
    else:
        raise ValueError(f'axis must be 0 or 1, got {axis}')

def _grid_if_not(ambiguous_grid):
    if isinstance(ambiguous_grid, GridShape):
        return ambiguous_grid
    else:
        return GridShape([ambiguous_grid])

def _compare_label_collections(collection1: LabelCollection, collection2: LabelCollection, use_object_equality=True):
    if use_object_equality:
        return collection1 == collection2
    else:
        return collection1.matches(collection2)

def _add_to_label_table_if_not_in_label_table(label_table: LabelTable, label_collection: LabelCollection,
                                              use_object_equality=True):
    """
    Note: inplace
    """
    # don't want to keep adding match over and over. need to check if match is already
    # stored in the common label table. must check two different ways depending on whether
    # we are using object equality or string consolidation
    if use_object_equality and label_collection not in label_table:
        label_table.append(label_collection)
    if (not use_object_equality) and (not label_table.contains(label_collection)):
        label_table.append(label_collection)