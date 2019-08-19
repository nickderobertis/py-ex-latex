from typing import Optional, Sequence, Union
from dero.latex.models.item import Item
from mixins.repr import ReprMixin
from dero.latex.table.models.panels.collection import PanelCollection
from dero.latex.table.models.texgen.alignment import ColumnsAlignment
from dero.latex.table.logic.table.build import build_tabular_content_from_panel_collection
from dero.latex.models.caption import Caption
from dero.latex.models.format.breaks import LineBreak
from dero.latex.texgen import _centering_str
from dero.latex.models.document import Document
from dero.latex.models.package import Package
from dero.latex.table.models.texgen.packages import default_packages
from dero.latex.models.landscape import Landscape
from dero.latex.models.label import Label
from dero.latex.models.section.base import TextAreaBase


class TableNotes(TextAreaBase, ReprMixin):
    name = 'tablenotes'

    def __init__(self, contents: Union[str, Sequence[str]]):
        super().__init__(self.name, contents, env_modifiers=f'[para, flushleft]')

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

    def __init__(self, table_content: Tabular, caption: Caption=None, below_text: TableNotes=None,
                 label: Optional[Label] = None):
        self.caption = caption
        items = [
            caption,
            table_content,
            below_text,
            label
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

    def __init__(self, three_part_table: ThreePartTable, centering=True, landscape=False):
        self.caption = three_part_table.caption
        self.landscape = landscape

        items = [
            _centering_str() if centering else None,
            three_part_table
        ]

        valid_items = [item for item in items if item is not None]

        content = LineBreak().join(valid_items)

        super().__init__(self.name, content)

    def __str__(self):
        content_with_env = super().__str__()
        if self.landscape:
            content_with_env = Landscape().wrap(str(content_with_env))
        return content_with_env

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
            below_text=table.below_text,
            label=Label(table.label) if table.label else None
        )
        return cls(three_part_table, *args, landscape=table.landscape, **kwargs)


class LTable(Table):
    name = 'ltable'


class TableDocument(Document):

    def __init__(self, content: Table, packages: [Package]=None, landscape: bool=False):
        if packages is None:
            packages = []

        packages += default_packages

        super().__init__(content, packages, landscape=landscape)

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
        return cls(tex_table, *args, **kwargs)
