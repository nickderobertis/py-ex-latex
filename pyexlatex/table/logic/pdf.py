from pyexlatex.table.models.panels.collection import PanelCollection
from pyexlatex.table.models.texgen.items import Table, TableDocument
from pyexlatex.logic.output.main import output_document_and_move


def output_panel_collection_to_tex(panel_collection: PanelCollection, out_folder: str, out_name: str='table',
                                   as_document=True,
                                   tabular_kwargs={}, three_part_table_kwargs={},
                                   table_kwargs={}, document_kwargs={}):
    if as_document:
        table_or_document = TableDocument.from_panel_collection(
            panel_collection,
            tabular_kwargs=tabular_kwargs,
            three_part_table_kwargs=three_part_table_kwargs,
            table_kwargs=table_kwargs,
            **document_kwargs
        )
    else:
        table_or_document = Table.from_panel_collection(
            panel_collection,
            tabular_kwargs=tabular_kwargs,
            three_part_table_kwargs=three_part_table_kwargs,
            **table_kwargs
        )


    output_document_and_move(
        table_or_document,
        outfolder=out_folder,
        outname=out_name,
        as_document=as_document,
        move_folder_name='Tables'
    )