import os
from typing import Union, List, Dict, Any, TYPE_CHECKING, Optional

from pyexlatex.typing import PyexlatexItems

if TYPE_CHECKING:
    from matplotlib.pyplot import Axes, Figure as PltFigure

from pyexlatex.figure.models.subfigure import Subfigure, Graphic
from pyexlatex.models.item import Item
from pyexlatex.models.caption import Caption
from pyexlatex.models.label import Label
from pyexlatex.logic.builder import build_figure_content
from pyexlatex.texgen.replacements.filename import latex_filename_replacements

from pyexlatex.models.commands.newenvironment import NewEnvironment
from pyexlatex.models.commands.begin import Begin
from pyexlatex.models.commands.end import End
from pyexlatex.models.environment import Environment
from pyexlatex.models.containeritem import ContainerItem

SubfigureOrGraphic = Union[Subfigure, Graphic]
SubfiguresOrGraphics = List[SubfigureOrGraphic]
PltFigureOrAxes = Union['Axes', 'PltFigure']
PltFigureOrAxesNameDict = Dict[str, PltFigureOrAxes]


class Figure(ContainerItem, Item):
    """
    Used for creating latex figures from images. Currently the main usage is the Figure class created with the method
    Figure.from_dict_of_names_and_filepaths. Pass a dictionary where the keys are names for subfigures and the values
    are filepaths where the image for the subfigure is located.

    """
    name = 'figure'

    def __init__(self, subfigures: SubfiguresOrGraphics, caption: Optional[PyexlatexItems] = None,
                 label: Optional[str] = None, centering: bool = True, position_str: Optional[str] = None,
                 landscape: bool = False):
        self.subfigures = subfigures
        self.caption = Caption(caption) if caption else None
        self.label = Label(label) if label else None
        self.centering = centering
        self.landscape = landscape

        self._remove_subfigure_elevate_contents_to_figure_if_single_subfigure()

        self.add_data_from_content(self.subfigures)

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
            self.data.begin_document_items.append(lfigure_def)
            self.env = Environment('lfigure')

    def __repr__(self):
        return f'<Figure(subfigures={self.subfigures}, caption={self.caption})>'

    def __iter__(self):
        for subfigure in self.subfigures:
            yield subfigure

    def __getitem__(self, item):
        return self.subfigures[item]

    def as_document(self, landscape=False):
        from pyexlatex.models.document import Document
        from pyexlatex.figure.packages import default_packages

        return Document(self, default_packages, landscape=landscape)

    def to_pdf_and_move(self, as_document=True, outfolder: str=None, outname: str=None,
                        landscape=False):
        from pyexlatex.logic.output.main import output_document_and_move
        from pyexlatex.models.document import Document

        to_output: Union[Figure, Document]
        to_output = self  # Figure
        if as_document:
            to_output = self.as_document(  # Document
                landscape=landscape if self.landscape == False else False  # don't apply landscape twice
            )

        if outfolder is None:
            outfolder = '.'
        if outname is None:
            outname = 'figure'
        else:
            outname = latex_filename_replacements(outname)

        output_document_and_move(
            to_output,
            outfolder,
            image_paths=self.data.filepaths,
            outname=outname,
            as_document=as_document,
            image_binaries=self.data.binaries
        )

    @classmethod
    def from_dict_of_names_and_filepaths(cls, filepath_name_dict: dict, figure_name: str=None,
                                         position_str_name_dict: dict=None, **kwargs):
        """
        Create a Figure from a dictionary where keys are names of subfigures and values are file paths

        :param filepath_name_dict: dictionary where keys are names of subfigures and values
            are the filepaths to the images for those subfigures.
        :param figure_name: name for overall figure
        :param position_str_name_dict: dictionary where keys are names of subfigures and values
            are the position strs for those figures, e.g. r'[t]{0.45\linewidth}'
        :param kwargs: kwargs for Figure
        :return: Figure
        """

        # TODO [#3]: for Figure, add possibility of passing grid shape rather than actual position str

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
            **kwargs
        )

    @classmethod
    def from_dict_of_names_and_plt_figures(cls, plt_fig_name_dict: PltFigureOrAxesNameDict, sources_outfolder: str,
                                           source_filetype: str = 'pdf',
                                           figure_name: str=None,
                                           position_str_name_dict: dict=None, **kwargs):
        """
        Create a Figure from a dictionary where keys are names of subfigures and values are matplotlib Figures
        or Axes

        :param plt_fig_name_dict: Key is display name in output figure, value is matplotlib axes or figure
        :param sources_outfolder: folder to output individual matplotlib figures
        :param source_filetype: Filetype for individual plt figures. The default is pdf. Use png or another
            image type if outputting complicated figures or performance may be affected when viewing the pdf.
        :param figure_name: name for overall figure
        :param position_str_name_dict: dictionary where keys are names of subfigures and values
            are the position strs for those figures, e.g. r'[t]{0.45\linewidth}'
        :param kwargs: kwargs for Figure
        :return: Figure
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
            **kwargs
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

        orig_width = self.subfigures[0].width

        # Elevate caption of sub-figure if there is no figure caption
        if self.caption is None and item_is_subfigure:
            self.caption = self.subfigures[0].caption

        # update width to original width
        graphic = Graphic(orig_graphic.filepaths[0], width=orig_width)

        # need to turn off centering to cover whole page
        self.centering = False

        self.subfigures = [graphic]

    def to_graphic_list(self) -> List[Graphic]:
        graphics: List[Graphic] = []
        for subfig_or_graphic in self.subfigures:
            if isinstance(subfig_or_graphic, Graphic):
                graphics.append(subfig_or_graphic)
            elif isinstance(subfig_or_graphic, Subfigure):
                graphics.append(subfig_or_graphic.graphic)
            else:
                raise ValueError(f'got other than Subfigure or Graphic in subfigures: '
                                 f'{subfig_or_graphic} of type {type(subfig_or_graphic)}')
        return graphics

def _get_plt_figure_from_axes_or_figure(plt_axes_or_fig: PltFigureOrAxes) -> 'PltFigure':
    # Both axes and figure have the get_figure method, however for the figure, it will return None
    possible_figure = plt_axes_or_fig.get_figure()
    if possible_figure is None:
        return plt_axes_or_fig  # had figure already
    else:
        return possible_figure # extracted figure from axes



