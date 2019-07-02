import os
from typing import Union, List, Dict, Any

from dero.latex.figure.models.subfigure import Subfigure, Graphic
from dero.latex.models.documentitem import DocumentItem
from dero.latex.models import Item
from dero.latex.models.caption import Caption
from dero.latex.models.label import Label
from dero.latex.models.landscape import Landscape
from dero.latex.logic.builder import build_figure_content
from dero.latex.texgen.replacements.filename import latex_filename_replacements
from matplotlib.pyplot import Axes, Figure as PltFigure
from dero.latex.models.commands.newenvironment import NewEnvironment
from dero.latex.models.commands.begin import Begin
from dero.latex.models.commands.end import End
from dero.latex.models.environment import Environment

SubfigureOrGraphic = Union[Subfigure, Graphic]
SubfiguresOrGraphics = List[SubfigureOrGraphic]
PltFigureOrAxes = Union[Axes, PltFigure]
PltFigureOrAxesNameDict = Dict[str, PltFigureOrAxes]

class Figure(DocumentItem, Item):
    """
    used for creating latex figures from images. Currently the main usage is the Figure class created with the method
    Figure.from_dict_of_names_and_filepaths. Pass a dictionary where the keys are names for subfigures and the values
    are filepaths where the image for the subfigure is located.

    """
    name = 'figure'

    def __init__(self, subfigures: SubfiguresOrGraphics, caption=None, label=None, centering=True, position_str=None,
                 landscape: bool=False):
        self.subfigures = subfigures
        self.caption = Caption(caption) if caption else None
        self.label = Label(label) if label else None
        self.centering = centering
        self.landscape = landscape

        self._remove_subfigure_elevate_contents_to_figure_if_single_subfigure()

        content = build_figure_content(
            self.subfigures,
            caption=self.caption,
            label=self.label,
            centering=self.centering,
            position_str=position_str
        )

        super().__init__(self.name, content)

        if landscape:
            lfigure_def = NewEnvironment(
                'lfigure',
                Begin('landscape') + Begin('figure'),
                End('figure') + End('landscape')
            )
            self.begin_document_items = [lfigure_def]
            self.env = Environment('lfigure')

    def __repr__(self):
        return f'<Figure(subfigures={self.subfigures}, caption={self.caption})>'

    def __iter__(self):
        for subfigure in self.subfigures:
            yield subfigure

    def __getitem__(self, item):
        return self.subfigures[item]

    def as_document(self, landscape=False):
        from dero.latex.models.document import Document
        from dero.latex.figure.packages import default_packages

        return Document(self, default_packages, landscape=landscape)

    def to_pdf_and_move(self, as_document=True, outfolder: str=None, outname: str=None,
                        landscape=False):
        from dero.latex.logic.pdf.main import document_to_pdf_and_move
        from dero.latex.models.document import Document

        to_output: Figure = self
        if as_document:
            to_output: Document = self.as_document(
                landscape=landscape if self.landscape == False else False  # don't apply landscape twice
            )

        if outfolder is None:
            outfolder = '.'
        if outname is None:
            outname = 'figure'
        else:
            outname = latex_filename_replacements(outname)

        document_to_pdf_and_move(
            to_output,
            outfolder,
            image_paths=self.filepaths,
            outname=outname,
            as_document=as_document,
            image_binaries=self.binaries
        )

    @property
    def filepaths(self) -> List[str]:
        return self._extract_items_from_subfigures_and_graphics_into_list('filepath')

    @property
    def source_paths(self) -> List[str]:
        return self._extract_items_from_subfigures_and_graphics_into_list('source_path')

    @property
    def binaries(self) -> List[bytes]:
        return self._extract_items_from_subfigures_and_graphics_into_list('binary')

    def _extract_items_from_subfigures_and_graphics_into_list(self, item_name: str) -> List[Any]:
        items = []
        for subfigure in self:
            if isinstance(subfigure, Subfigure):
                items.append(getattr(subfigure.graphic, item_name))
            elif isinstance(subfigure, Graphic):
                items.append(getattr(subfigure, item_name))
            else:
                raise ValueError(f'must pass Subfigures or Graphics to Figure. got type {type(subfigure)}')
        return items


    @classmethod
    def from_dict_of_names_and_filepaths(cls, filepath_name_dict: dict, figure_name: str=None,
                                         position_str_name_dict: dict=None, label=None, centering=True,
                                         landscape: bool = False):
        """

        Args:
            filepath_name_dict: dictionary where keys are names of subfigures and values
                                are the filepaths to the images for those subfigures.
            figure_name: name for overall figure
            position_str_name_dict: dictionary where keys are names of subfigures and values
                                are the position strs for those figures, e.g. r'[t]{0.45\linewidth}'

        Returns:

        """

        # TODO: add possibility of passing grid shape rather than actual position str

        if position_str_name_dict is None:
            position_str_name_dict = {}

        subfigures = []
        for name, filepath in filepath_name_dict.items():
            subfigures.append(
                Subfigure(
                    filepath,
                    caption=name,
                    position_str=position_str_name_dict[name] if name in position_str_name_dict else r'[t]{0.45\linewidth}'
                )
            )

        return cls(
            subfigures,
            caption=figure_name,
            label=label,
            centering=centering,
            landscape=landscape
        )

    @classmethod
    def from_dict_of_names_and_plt_figures(cls, plt_fig_name_dict: PltFigureOrAxesNameDict, sources_outfolder: str,
                                           source_filetype: str = 'pdf',
                                           figure_name: str=None,
                                           position_str_name_dict: dict=None, label=None, centering=True,
                                           landscape: bool = False):
        """

        Args:
            plt_fig_name_dict: Key is display name in output figure, value is matplotlib axes or figure
            sources_outfolder: folder to output individual plt figures
            source_filetype: Filetype for individual plt figures. The default is pdf. Use png or another image type if
                outputting complicated figures or performance may be affected when viewing the pdf.
            figure_name: name for overall figure
            position_str_name_dict: dictionary where keys are names of subfigures and values
                are the position strs for those figures, e.g. r'[t]{0.45\linewidth}'
            label:
            centering:
            landscape:

        Returns: Figure

        """

        filepath_name_dict = {}  # store outputted filepaths of sources to pass to from_dict_of_names_and_filepaths
        for name, plt_figure_or_axes in plt_fig_name_dict.items():
            plt_figure = _get_plt_figure_from_axes_or_figure(plt_figure_or_axes)
            outpath = os.path.join(sources_outfolder, f'{latex_filename_replacements(name)}.{source_filetype}')
            plt_figure.savefig(outpath)
            filepath_name_dict[name] = outpath

        return cls.from_dict_of_names_and_filepaths(
            filepath_name_dict,
            figure_name=figure_name,
            position_str_name_dict=position_str_name_dict,
            label=label,
            centering=centering,
            landscape=landscape
        )



    def _remove_subfigure_elevate_contents_to_figure_if_single_subfigure(self):
        """
        If there is a single subfigure, leaving in subfigure format results in very small output. Must strip
        out subfigure layer, leaving only a figure with a graphic, then it can fill the page.
        :return:
        """
        if len(self.subfigures) != 1:
            return

        self.subfigures: List[Union[Subfigure, Graphic]]

        if hasattr(self.subfigures[0], 'graphic'):
            # got subfigure
            item_is_subfigure = True
            orig_graphic = self.subfigures[0].graphic
        else:
            # got graphic
            item_is_subfigure = False
            orig_graphic = self.subfigures[0]

        # Elevate caption of sub-figure if there is no figure caption
        if self.caption is None and item_is_subfigure:
            self.caption = self.subfigures[0].caption

        # update width to whole page
        graphic = Graphic(orig_graphic.filepath, width=r'1.1\paperwidth')

        # need to turn off centering to cover whole page
        self.centering = False

        self.subfigures = [graphic]


def _get_plt_figure_from_axes_or_figure(plt_axes_or_fig: PltFigureOrAxes) -> PltFigure:
    # Both axes and figure have the get_figure method, however for the figure, it will return None
    possible_figure = plt_axes_or_fig.get_figure()
    if possible_figure is None:
        return plt_axes_or_fig  # had figure already
    else:
        return possible_figure # extracted figure from axes



