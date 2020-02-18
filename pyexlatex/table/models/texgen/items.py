from typing import Optional, Sequence, Union, List
import pandas as pd
from pyexlatex.models.item import Item
from pyexlatex.models.containeritem import ContainerItem
from mixins.repr import ReprMixin
from pyexlatex.table.models.panels.collection import PanelCollection
from pyexlatex.table.models.texgen.tabularbase import BaseTabular
from pyexlatex.table.models.texgen.alignment import ColumnsAlignment
from pyexlatex.table.logic.table.build import build_tabular_content_from_panel_collection
from pyexlatex.models.caption import Caption
from pyexlatex.texgen import _centering_str
from pyexlatex.models.document import Document
from pyexlatex.models.package import Package
from pyexlatex.models.landscape import Landscape
from pyexlatex.models.label import Label
from pyexlatex.models.section.base import TextAreaBase
from pyexlatex.table.models.data.table import DataTable


class TableNotes(TextAreaBase, ReprMixin):
    name = 'tablenotes'

    def __init__(self, contents: Union[str, Sequence[str]]):
        super().__init__(self.name, contents, env_modifiers=f'[para, flushleft]')


class Tabular(ContainerItem, Item, ReprMixin, BaseTabular):
    """
    The main part of a LaTeX table which contains the rows and columns.
    """
    name = 'tabular'
    repr_cols = ['align']

    def __init__(self, content, align: Optional[Union[ColumnsAlignment, str]] = None):
        if not isinstance(content, (list, tuple)):
            content = [content]
        self.align = self._get_columns_alignment_from_passed_align(content, align)
        self.add_package('booktabs')  # Remove this once booktabs is added in cmidrule and others
        self.add_data_from_content(self.align)
        super().__init__(self.name, content, env_modifiers=self._wrap_with_braces(str(self.align)))

    @classmethod
    def from_panel_collection(cls, panel_collection: PanelCollection, align: Optional[ColumnsAlignment] = None,
                 mid_rules=True):
        align = align if align is not None else ColumnsAlignment(num_columns=panel_collection.num_columns)
        obj = cls([[0]], align=align)  # dummy content
        obj.panel_collection = panel_collection
        obj.contents = build_tabular_content_from_panel_collection(panel_collection, mid_rule=mid_rules)

        return obj

    @classmethod
    def from_df(cls, df: pd.DataFrame, align: Optional[ColumnsAlignment] = None, **dt_from_df_kwargs):
        dt = DataTable.from_df(df, **dt_from_df_kwargs)
        return cls(dt, align=align)


class ThreePartTable(TextAreaBase, ReprMixin):
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
        content = [item for item in items if item is not None]

        super().__init__(self.name, content)

    @classmethod
    def from_panel_collection(cls, panel_collection: PanelCollection, *args, tabular_kwargs={}, **kwargs):
        tabular = Tabular.from_panel_collection(panel_collection, **tabular_kwargs)

        caption: Optional[Caption]
        if panel_collection.name is not None:
            caption = Caption(panel_collection.name)
        else:
            caption = None

        return cls(tabular, caption=caption, **kwargs)

class Table(TextAreaBase, ReprMixin):
    name = 'table'
    repr_cols = ['caption']

    def __init__(self, three_part_table: ThreePartTable, centering=True, landscape=False):
        self.caption = three_part_table.caption
        self.landscape = landscape

        items = [
            _centering_str() if centering else None,
            three_part_table
        ]

        content = [item for item in items if item is not None]

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
        from pyexlatex.table.models.table.table import Table as TableModel
        table: TableModel
        tabular = Tabular.from_panel_collection(
            table.panels,
            align=table.align,
            mid_rules=table.mid_rules
        )

        three_part_table = ThreePartTable(
            tabular,
            caption=table.caption,
            below_text=table.below_text,
            label=table.label
        )
        obj = cls(three_part_table, *args, landscape=table.landscape, **kwargs)
        obj.add_data_from_content(table)
        return obj



class LTable(Table):
    name = 'ltable'

    def __str__(self):
        # Skip landscape wrapping being done in Table as it is already handled by ltable definition
        return TextAreaBase.__str__(self)


class TableDocument(Document):

    def __init__(self, content: Table, packages: List[Package]=None, landscape: bool=False):
        from pyexlatex.table.models.texgen.packages import default_packages

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
        from pyexlatex.table.models.table.table import Table as TableModel
        table: TableModel
        tex_table = Table.from_table_model(table, *args, **kwargs)
        obj = cls(tex_table, *args, **kwargs)
        obj.add_data_from_content(table)
        return obj
