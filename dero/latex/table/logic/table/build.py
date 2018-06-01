from dero.latex.table.models.panels.collection import PanelCollection
from dero.latex.table.models.table.row import Row
from dero.latex.table.models.texgen.lines import TopRule, MidRule, BottomRule, TableLine
from dero.latex.table.models.texgen.breaks import TableRowBreak

def build_tabular_content_from_panel_collection(panel_collection: PanelCollection, mid_rule=True):
    rows: [Row, TableLine] = _build_tabular_rows_from_panel_collection(
        panel_collection=panel_collection,
        mid_rule=mid_rule
    )

    content: str = _build_tabular_str_from_rows_and_lines(rows)

    return content



def _build_tabular_rows_from_panel_collection(panel_collection: PanelCollection, mid_rule=True):
    rows: [Row, TableLine] = [TopRule()]
    for panel in panel_collection.iterpanels():
        rows += panel.rows
        if mid_rule:
            rows.append(MidRule())

    rows.append(BottomRule())
    return rows


def _build_tabular_str_from_rows_and_lines(rows_and_lines: [Row, TableLine], break_size_adjustment: str=None):
    line_break = TableRowBreak(break_size_adjustment)
    return line_break.join(rows_and_lines)

