from dero.latex.models.item import Item
from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.panels.collection import PanelCollection
from dero.latex.table.models.texgen.alignment import ColumnsAlignment
from dero.latex.table.logic.table.build import build_tabular_content_from_panel_collection
from dero.latex.models.caption import Caption
from dero.latex.table.models.texgen.breaks import LineBreak
from dero.latex.texgen import _centering_str
from dero.latex.models.document import Document
from dero.latex.models.package import Package
from dero.latex.table.models.texgen.packages import default_packages
from dero.latex.texgen import general_latex_replacements


class TableNotes(Item, ReprMixin):
    name = 'tablenotes'

    def __init__(self, content: str):
        content = general_latex_replacements(content)
        super().__init__(self.name, content, env_modifiers=f'[para, flushleft]')

class Tabular(Item, ReprMixin):
    name = 'tabular'
    repr_cols = ['align']

    def __init__(self, panel_collection: PanelCollection, align: ColumnsAlignment=None,
                 mid_rules=True):
        self.align = align if align is not None else ColumnsAlignment(num_columns=panel_collection.num_columns)
        self.panel_collection = panel_collection

        content = build_tabular_content_from_panel_collection(panel_collection, mid_rule=mid_rules)

        super().__init__(self.name, content, env_modifiers=f'{{{self.align}}}')

class ThreePartTable(Item, ReprMixin):
    name = 'threeparttable'
    repr_cols = ['caption']

    def __init__(self, table_content: Tabular, caption: Caption=None, below_text: TableNotes=None):
        self.caption = caption
        items = [
            caption,
            table_content,
            below_text
        ]
        valid_items = [item for item in items if item is not None]

        content = LineBreak().join(valid_items)
        super().__init__(self.name, content)

    @classmethod
    def from_panel_collection(cls, panel_collection: PanelCollection, *args, tabular_kwargs={}, **kwargs):
        tabular = Tabular(panel_collection, **tabular_kwargs)

        if panel_collection.name is not None:
            caption = Caption(panel_collection.name)
        else:
            caption = None

        return cls(tabular, caption=caption, *args, **kwargs)

class Table(Item, ReprMixin):
    name = 'table'
    repr_cols = ['caption']

    def __init__(self, three_part_table: ThreePartTable, centering=True):
        self.caption = three_part_table.caption

        items = [
            _centering_str() if centering else None,
            three_part_table
        ]

        valid_items = [item for item in items if item is not None]

        content = LineBreak().join(valid_items)
        super().__init__(self.name, content)

    @classmethod
    def from_panel_collection(cls, panel_collection: PanelCollection, *args, tabular_kwargs={},
                              three_part_table_kwargs={}, **kwargs):
        three_part_table = ThreePartTable.from_panel_collection(
            panel_collection,
            tabular_kwargs=tabular_kwargs,
            **three_part_table_kwargs
        )
        return cls(three_part_table, *args, **kwargs)

    @classmethod
    def from_table_model(cls, table, *args, **kwargs):
        from dero.latex.table.models.table.table import Table as TableModel
        table: TableModel
        tabular = Tabular(
            table.panels,
            align=table.align,
            mid_rules=table.mid_rules
        )

        three_part_table = ThreePartTable(
            tabular,
            caption=table.caption,
            below_text=table.below_text
        )
        return cls(three_part_table, *args, **kwargs)

class TableDocument(Document):

    def __init__(self, content: Table, packages: [Package]=None, landscape: bool=False):
        if packages is None:
            packages = []

        packages += default_packages

        super().__init__(packages, content, landscape=landscape)

    @classmethod
    def from_panel_collection(cls, panel_collection: PanelCollection, *args, tabular_kwargs={},
                              three_part_table_kwargs={}, table_kwargs={}, **kwargs):
        table = Table.from_panel_collection(
            panel_collection,
            tabular_kwargs=tabular_kwargs,
            three_part_table_kwargs=three_part_table_kwargs,
            **table_kwargs
        )
        return cls(table, *args, **kwargs)

    @classmethod
    def from_table_model(cls, table, *args, **kwargs):
        from dero.latex.table.models.table.table import Table as TableModel
        table: TableModel
        tex_table = Table.from_table_model(table, *args, **kwargs)
        return cls(tex_table, *args, landscape=table.landscape, **kwargs)
