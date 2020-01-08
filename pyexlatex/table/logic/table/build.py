from typing import Union, List, Sequence

from pyexlatex.table.models.panels.collection import PanelCollection
from pyexlatex.table.models.table.row import Row
from pyexlatex.table.models.texgen.lines import TopRule, MidRule, BottomRule, TableLine
from pyexlatex.models.format.breaks import TableLineBreak, LineBreak

def build_tabular_content_from_panel_collection(panel_collection: PanelCollection, mid_rule=True):
    rows: List[Union[Row, TableLine]] = _build_tabular_rows_from_panel_collection(
        panel_collection=panel_collection,
        mid_rule=mid_rule
    )

    content: str = _build_tabular_str_from_rows_and_lines(rows)

    return content



def _build_tabular_rows_from_panel_collection(panel_collection: PanelCollection, mid_rule=True):
    rows: List[Union[Row, TableLine]] = [TopRule()]
    panels = list(panel_collection.iterpanels())
    for i, panel in enumerate(panels):
        rows += panel.rows
        # add mid rule when:
        # boolean is turned on,
        # not the last loop,
        # and panel is not made entirely of spacers,
        # and next panel is not made entirely of spacers
        if mid_rule and i != len(panels) - 1 and not panel.is_spacer and not panels[i + 1].is_spacer:
            rows.append(MidRule())

    rows.append(BottomRule())
    return rows


def _build_tabular_str_from_rows_and_lines(rows_and_lines: Sequence[Union[Row, TableLine]], break_size_adjustment: str=None):
    output_str = ''
    for i, row_or_line in enumerate(rows_and_lines):
        end = _get_break_by_type_of_instance(row_or_line, break_size_adjustment=break_size_adjustment)
        output_str += f'{row_or_line}{end}'
    return output_str


def _get_break_by_type_of_instance(row_or_line: Union[Row, TableLine], break_size_adjustment: str=None):
    table_row_break = TableLineBreak(break_size_adjustment)
    line_break = LineBreak()
    if isinstance(row_or_line, TableLine):
        end = line_break
    elif isinstance(row_or_line, Row):
        end = table_row_break
    else:
        raise NotImplementedError(f'could not determine type of break for row or line type {type(row_or_line)}')

    return end

