from copy import deepcopy
from typing import Union, AnyStr, List, TYPE_CHECKING, Optional, Dict, Callable
import pandas as pd
import numpy as np

from pyexlatex.table.models.panels.grid import PanelGrid
from pyexlatex.texgen.packages.columntypes import ColumnTypesPackage

if TYPE_CHECKING:
    from pyexlatex.table.models.texgen.items import ColumnsAlignment

from mixins.repr import ReprMixin
from pyexlatex.table.models.panels.collection import PanelCollection, Panel
from pyexlatex.table.models.labels.table import LabelTable, LabelCollection
from pyexlatex.table.models.table.caption import Caption
from pyexlatex.logic.output.main import output_document_and_move
from pyexlatex.texgen.replacements.filename import latex_filename_replacements
from pyexlatex.models.documentitem import DocumentItem
from pyexlatex.models.commands.newenvironment import NewEnvironment
from pyexlatex.models.commands.begin import Begin
from pyexlatex.models.commands.end import End
from pyexlatex.models.documentsetup import DocumentSetupData
from pyexlatex.models.label import Label


class Table(DocumentItem, ReprMixin):
    """
    An object for creating latex tables. Easiest way to create is with Table.from_list_of_lists_of_dfs,
    but for more control, construct Panel objects and use Table.from_panel_list
    """
    repr_cols = ['caption', 'above_text', 'panels', 'below_text']
    _align: Union['ColumnsAlignment', str]

    def __init__(self, panels: PanelCollection, caption: str=None, above_text: str=None, below_text: str=None,
                 align: str = None, mid_rules=True, landscape=False, label: Optional[str] = None):
        """

        :param panels: list of Panels
        :param caption: overall caption to place at top of table
        :param above_text: Not yet implemented
        :param below_text: text to place below table
        :param align: Can take any string that would normally used in tabular (i.e. rrr for three columns right aligned)
                        as well as . for decimal aligned, and L{<width>), C{<width>}, and R{<width>} (i.e. L{3cm})
                        for left, center, and right aligned fixed width. Default is first column left aligned,
                        rest center aligned.
        :param mid_rules: whether to add mid rules between panels
        :param landscape: whether to output landscape tex
        :param label: label for table to be referenced in text
        """
        from pyexlatex.table.models.texgen.items import TableNotes
        self.panels = panels
        self.caption = Caption(caption)
        self.above_text = _set_above_text(above_text)
        self.below_text = TableNotes(below_text) if below_text is not None else None
        self.align = align
        self.mid_rules = mid_rules
        self.landscape = landscape
        self.label = Label(label) if label else None
        self.data = DocumentSetupData()
        self.data.packages.extend(['threeparttable', 'booktabs', ColumnTypesPackage()])
        self.set_begin_document_items(landscape)

    def __str__(self):
        from pyexlatex.logic.builder import build
        tex_obj = self.tex_obj(as_document=False)

        # TODO [#18]: restructure table module so that it works like others where items are tex generators
        #
        # Until then, need to manually call build as it won't carry through to the separate tex generator
        build(tex_obj)

        return str(tex_obj)

    def to_tex(self, as_document=True):
        tex_generator = self.tex_obj(as_document=as_document)
        return str(tex_generator)

    def tex_obj(self, as_document: bool = True, as_single_tabular: bool = False, as_panel_tabular_list: bool = False):
        from pyexlatex.table.models.texgen.items import TableDocument, Table as TexTable, LTable, Tabular

        if sum([as_document, as_single_tabular, as_panel_tabular_list]) > 1:
            raise ValueError('must pass only one of as_document, as_single_tabular, as_panel_tabular_list')

        class_factory: Callable[['Table'], Union[TableDocument, Tabular, List[Tabular], TexTable, LTable]]
        if as_document:
            class_factory = TableDocument.from_table_model
        elif as_single_tabular:
            def class_factory(table: 'Table') -> Tabular:
                tabular = Tabular.from_panel_collection(
                    table.panels,
                    align=table.align,
                    mid_rules=table.mid_rules
                )
                return tabular
        elif as_panel_tabular_list:
            def class_factory(table: 'Table') -> List[Tabular]:
                from pyexlatex.table.models.table.section import TableSection

                table = deepcopy(table)  # avoid modifying original table
                tabulars: List[Tabular] = []
                headers: TableSection = TableSection([])
                if table.panels.has_column_labels:
                    # Get headers if needed for later, as table may change throughout this process
                    headers = deepcopy(table.panels.rows[0])
                for i, panel in enumerate(table.panels.iterpanels(add_panel_order_label=False)):
                    use_panel = panel
                    if panel.is_spacer:
                        continue
                    if table.panels.has_column_labels:
                        # If there are column labels for the panel collection, need to skip first panel
                        # but then take its values and put as headers for all other panels
                        if i == 0:
                            continue
                        use_panel = deepcopy(panel)  # avoid modifying existing panel
                        use_headers: TableSection = deepcopy(headers)
                        new_grid = np.concatenate([PanelGrid([use_headers]), use_panel.panel_grid], axis=0)
                        use_panel.panel_grid = new_grid
                    pc = PanelCollection(
                        [use_panel],
                        name=use_panel.name,
                        pad_rows=0
                    )
                    tabular = Tabular.from_panel_collection(
                        pc,
                        align=table.align,
                        mid_rules=table.mid_rules
                    )
                    tabulars.append(tabular)
                return tabulars
        else:
            if self.landscape:
                class_factory = LTable.from_table_model
            else:
                class_factory = TexTable.from_table_model

        tex_generator = class_factory(self)
        return tex_generator

    def to_pdf_and_move(self, outfolder, outname=None,
                              move_folder_name='Tables', as_document=True):
        tex = self.to_tex(as_document=as_document)

        if outname is None:
            outname = self.caption

        outname = latex_filename_replacements(outname)

        output_document_and_move(
            tex,
            outfolder=outfolder,
            outname=outname,
            move_folder_name=move_folder_name,
            as_document=as_document
        )

    @classmethod
    def from_panel_list(cls, panels: List[Panel], label_consolidation: str='object', enforce_label_order=True,
                        top_left_corner_labels: Union[LabelTable, LabelCollection, List[AnyStr], AnyStr] = None,
                        pad_rows: int=1, pad_columns: int=1, caption: str=None, above_text: str=None,
                        below_text: str=None, align: str = None, mid_rules=True, landscape=False,
                        label: Optional[str] = None):
        """
        Note: to quickly create latex tables, use Table.from_list_of_lists_of_dfs to pass
        pandas DataFrames directly. Use this method when more control is needed than is provided by that method.
        Construct Panels individually, either directly from DataFrames with Panel.from_df_list, or for even more
        control, use DataTable.from_df and override labels with custom LabelTables.

        :param panels: list of Panels
        :param label_consolidation: pass 'object' to to avoid consolidating labels. pass 'str' to consolidate if
                                    column or index contents are identical within a column or row of DataFrames
        :param enforce_label_order: pass False to allow consolidating lower labels even if upper labels do not match.
                                    e.g. if labels on one table are [['Top1'], ['Bot1', 'Bot2']], then labels on the other
                                    table are [['Top2'], ['Bot1', 'Bot2']], consolidated labels when passing False will be
                                    ['Bot1', 'Bot2'], while when passing True, no labels will be consolidated. Under True,
                                    will start from the top label, then stop consolidating once it has a mismatch.
        :param top_left_corner_labels: additional labels to place in the top left corner. pass a single string
                                       or a list of strings for convenience. a list of strings will be create labels
                                       which span the gap horizontally and go downwards, one label per row. pass
                                       LabelCollection or LabelTable for more control.
        :param pad_rows: horizontal spacing to put between panels
        :param pad_columns: vertical spacing to put between TableSections
        :param caption: overall caption to place at top of table
        :param above_text: Not yet implemented
        :param below_text: text to place below table
        :param align: Can take any string that would normally used in tabular (i.e. rrr for three columns right aligned
                        as well as L{<width>), C{<width>}, and R{<width>} (i.e. L{3cm}) for left, center, and right aligned
                        fixed width. Default is first column left aligned, rest center aligned.
        :param mid_rules: whether to add mid rules between panels
        :param landscape: whether to output landscape tex
        :param label: label for table to be referenced in text
        :return:
        """
        panel_collection = PanelCollection(
            panels,
            label_consolidation=label_consolidation,
            enforce_label_order=enforce_label_order,
            top_left_corner_labels=top_left_corner_labels,
            pad_rows=pad_rows,
            pad_columns=pad_columns,
            name=caption
        )

        return cls(
            panel_collection,
            caption=caption,
            above_text=above_text,
            below_text=below_text,
            align=align,
            mid_rules=mid_rules,
            landscape=landscape,
            label=label
        )

    @classmethod
    def from_list_of_lists_of_dfs(cls, df_list_of_lists: List[List[pd.DataFrame]],
                                  panel_names: List[str]=None, shape: tuple=None,
                                  include_columns=True, include_index=False,
                                  label_consolidation: str = 'str', enforce_label_order=True,
                                  top_left_corner_labels: Union[LabelTable, LabelCollection, List[AnyStr], AnyStr] = None,
                                  pad_rows: int = 1, pad_columns: int = 1, caption: str = None, above_text: str = None,
                                  below_text: str = None, align: str = None, mid_rules=True, landscape=False,
                                  label: Optional[str] = None,
                                  data_table_kwargs={}
                                  ):
        """
        To create a single panel table, pass a single list within
        a list of DataFrames, e.g. [[df1, df2]] then shape will specify how the DataFrames will
        be organized in the Panel. If you pass two lists within the outer list, then shape will
        apply to each Panel. So [[df1, df2], [df3, df4]] with shape=(1,2) create a two Panel table
        with two tables placed within each panel going horizontally, so that the overall shape is (2,2).

        Note: convenience method for if not much control over table is needed.
        To apply different options to each panel, construct them individually using
        Panel.from_df_list or sub panels individually with DataTable.from_df then make modifications

        :param df_list_of_lists: list of lists of pandas DataFrame
        :param panel_names: list of panel names. Must be of same length as outer list in df_list_of_lists
        :param shape: tuple of (rows, columns) to arrange DataFrames. They will be placed from left to right,
                      then from top to bottom.
                      passsing None defaults one column, as many rows as DataFrames.
                      Note: this is for each panel. To apply a different shape to each Panel, construct Panels individually
                      and pass to Table.from_panel_list
        :param include_columns:
        :param include_index:
        :param label_consolidation: pass 'object' to to avoid consolidating labels. pass 'str' to consolidate if
                                    column or index contents are identical within a column or row of DataFrames
        :param top_left_corner_labels: additional labels to place in the top left corner. pass a single string
                                       or a list of strings for convenience. a list of strings will be create labels
                                       which span the gap horizontally and go downwards, one label per row. pass
                                       LabelCollection or LabelTable for more control.
        :param enforce_label_order: pass False to allow consolidating lower labels even if upper labels do not match.
                                    e.g. if labels on one table are [['Top1'], ['Bot1', 'Bot2']], then labels on the other
                                    table are [['Top2'], ['Bot1', 'Bot2']], consolidated labels when passing False will be
                                    ['Bot1', 'Bot2'], while when passing True, no labels will be consolidated. Under True,
                                    will start from the top label, then stop consolidating once it has a mismatch.
        :param pad_rows: horizontal spacing to put between panels
        :param pad_columns: vertical spacing to put between TableSections
        :param caption: overall caption to place at top of table
        :param above_text: Not yet implemented
        :param below_text: text to place below table
        :param align: Can take any string that would normally used in tabular (i.e. rrr for three columns right aligned
                        as well as L{<width>), C{<width>}, and R{<width>} (i.e. L{3cm}) for left, center, and right aligned
                        fixed width. Default is first column left aligned, rest center aligned.
        :param mid_rules: whether to add mid rules between panels
        :param landscape: whether to output landscape tex
        :param label: label for table to be referenced in text
        :param data_table_kwargs: kwargs to be passed to DataTable.from_df. Same kwargs will be passed to
                                  all data tables.
        :return:
        """
        panel_collection = PanelCollection.from_list_of_lists_of_dfs(
            df_list_of_lists,
            panel_names=panel_names,
            panel_kwargs=dict(
                shape=shape,
                include_columns=include_columns,
                include_index=include_index,
            ),
            label_consolidation=label_consolidation,
            enforce_label_order=enforce_label_order,
            top_left_corner_labels=top_left_corner_labels,
            pad_rows=pad_rows,
            pad_columns=pad_columns,
            name=caption,
            data_table_kwargs=data_table_kwargs
        )

        return cls(
            panel_collection,
            caption=caption,
            above_text=above_text,
            below_text=below_text,
            align=align,
            mid_rules=mid_rules,
            landscape=landscape,
            label=label
        )

    @classmethod
    def from_panel_name_df_dict(cls, panel_name_df_dict: Dict[str, pd.DataFrame],
                                include_columns=True, include_index=False,
                                label_consolidation: str = 'str', enforce_label_order=True,
                                top_left_corner_labels: Union[LabelTable, LabelCollection, List[AnyStr], AnyStr] = None,
                                pad_rows: int = 1, caption: str = None, above_text: str = None,
                                below_text: str = None, align: str = None, mid_rules=True, landscape=False,
                                label: Optional[str] = None,
                                data_table_kwargs={}
                                ):
        """
        Convenience method for when there is only one DataFrame per panel. All options will be applied all panels and
        DataTables.
        To apply different options to each panel, construct them individually using
        Panel.from_df_list or sub panels individually with DataTable.from_df then make modifications

        :param panel_name_df_dict: dictionary where keys are names of panels, and values are DataFrames to put in panels
                                   (only one DataFrame per panel. Use another method if more control is needed)
        :param include_columns:
        :param include_index:
        :param label_consolidation: pass 'object' to to avoid consolidating labels. pass 'str' to consolidate if
                                    column or index contents are identical within a column or row of DataFrames
        :param top_left_corner_labels: additional labels to place in the top left corner. pass a single string
                                       or a list of strings for convenience. a list of strings will be create labels
                                       which span the gap horizontally and go downwards, one label per row. pass
                                       LabelCollection or LabelTable for more control.
        :param enforce_label_order: pass False to allow consolidating lower labels even if upper labels do not match.
                                    e.g. if labels on one table are [['Top1'], ['Bot1', 'Bot2']], then labels on the other
                                    table are [['Top2'], ['Bot1', 'Bot2']], consolidated labels when passing False will be
                                    ['Bot1', 'Bot2'], while when passing True, no labels will be consolidated. Under True,
                                    will start from the top label, then stop consolidating once it has a mismatch.
        :param pad_rows: horizontal spacing to put between panels
        :param caption: overall caption to place at top of table
        :param above_text: Not yet implemented
        :param below_text: text to place below table
        :param align: Can take any string that would normally used in tabular (i.e. rrr for three columns right aligned
                        as well as L{<width>), C{<width>}, and R{<width>} (i.e. L{3cm}) for left, center, and right aligned
                        fixed width. Default is first column left aligned, rest center aligned.
        :param mid_rules: whether to add mid rules between panels
        :param landscape: whether to output landscape tex
        :param label: label for table to be referenced in text
        :param data_table_kwargs: kwargs to be passed to DataTable.from_df. Same kwargs will be passed to
                                  all data tables.
        :return:
        """

        df_list_of_lists = []
        panel_names = []
        for panel_name, df in panel_name_df_dict.items():
            df_list_of_lists.append([df])
            panel_names.append(panel_name)

        return cls.from_list_of_lists_of_dfs(
            df_list_of_lists,
            panel_names=panel_names,
            include_columns=include_columns,
            include_index=include_index,
            label_consolidation=label_consolidation,
            enforce_label_order=enforce_label_order,
            top_left_corner_labels=top_left_corner_labels,
            pad_rows=pad_rows,
            caption=caption,
            above_text=above_text,
            below_text=below_text,
            align=align,
            mid_rules=mid_rules,
            landscape=landscape,
            data_table_kwargs=data_table_kwargs,
            label=label
        )

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, align: Union['ColumnsAlignment', str]):
        from pyexlatex.table.models.texgen.items import ColumnsAlignment
        if align is None:
            self._align = ColumnsAlignment(num_columns=self.panels.num_columns)
        elif isinstance(align, ColumnsAlignment):
            self._align = align
        elif isinstance(align, str):
            self._align = ColumnsAlignment.from_alignment_str(align, num_columns=self.panels.num_columns)
        else:
            raise NotImplementedError(f'could not create align from {align}')

    def set_begin_document_items(self, landscape: bool):
        begin_doc_items = []
        if landscape:
            ltable_def = NewEnvironment(
                'ltable',
                Begin('landscape') + Begin('table'),
                End('table') + End('landscape')
            )
            begin_doc_items.append(ltable_def)
        self.data.begin_document_items.extend(begin_doc_items) 





def _set_above_text(above_text):
    # TODO [#19]: handle above text in tables
    if above_text is not None:
        raise NotImplementedError('will add above text in a future release')
