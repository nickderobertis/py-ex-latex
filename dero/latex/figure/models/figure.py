from typing import Union, List

from dero.latex.figure.models.subfigure import Subfigure, Graphic
from dero.latex.models import Item
from dero.latex.models.caption import Caption
from dero.latex.models.label import Label
from dero.latex.logic.builder import build_figure_content
from dero.latex.models.document import Document

SubfigureOrGraphic = Union[Subfigure, Graphic]
SubfiguresOrGraphics = List[SubfigureOrGraphic]

class Figure(Item):
    """
    used for creating latex figures from images. Currently the main usage is the Figure class created with the method
    Figure.from_dict_of_names_and_filepaths. Pass a dictionary where the keys are names for subfigures and the values
    are filepaths where the image for the subfigure is located.

    """
    name = 'figure'

    def __init__(self, subfigures: SubfiguresOrGraphics, caption=None, label=None, centering=True, position_str=None):
        self.subfigures = subfigures
        self.caption = Caption(caption) if caption else None
        self.label = Label(label) if label else None
        self.centering = centering

        self._remove_subfigure_elevate_contents_to_figure_if_single_subfigure()

        content = build_figure_content(
            self.subfigures,
            caption=self.caption,
            label=self.label,
            centering=self.centering,
            position_str=position_str
        )

        super().__init__(self.name, content)

    def __repr__(self):
        return f'<Figure(subfigures={self.subfigures}, caption={self.caption})>'

    def __iter__(self):
        for subfigure in self.subfigures:
            yield subfigure

    def __getitem__(self, item):
        return self.subfigures[item]

    def as_document(self, landscape=False):
        from dero.latex.models.package import Package

        simple_package_strs = [
            'caption',
            'subcaption',
            'graphicx',
            'pdflscape'
        ]
        simple_packages = [Package(str_) for str_ in simple_package_strs]

        packages = simple_packages + [
            Package('geometry', modifier_str='margin=0.1in')
        ]

        return Document(packages, self, landscape=landscape)

    def to_pdf_and_move(self, as_document=True, outfolder: str=None, outname: str=None,
                        landscape=False):
        from dero.latex.logic.pdf import _document_to_pdf_and_move

        to_output: Figure = self
        if as_document:
            to_output: Document = self.as_document(landscape=landscape)

        if outfolder is None:
            outfolder = '.'
        if outname is None:
            outname = 'figure'

        _document_to_pdf_and_move(
            to_output,
            outfolder,
            image_paths=self.filepaths,
            outname=outname,
            as_document=as_document
        )

    @property
    def filepaths(self):
        filepaths = []
        for subfigure in self:
            if isinstance(subfigure, Subfigure):
                filepaths.append(subfigure.graphic.filepath)
            elif isinstance(subfigure, Graphic):
                filepaths.append(subfigure.filepath)
            else:
                raise ValueError(f'must pass Subfigures or Graphics to Figure. got type {type(subfigure)}')
        return filepaths

    @property
    def source_paths(self):
        source_paths = []
        for subfigure in self:
            if isinstance(subfigure, Subfigure):
                source_paths.append(subfigure.graphic.source_path)
            elif isinstance(subfigure, Graphic):
                source_paths.append(subfigure.source_path)
            else:
                raise ValueError(f'must pass Subfigures or Graphics to Figure. got type {type(subfigure)}')
        return source_paths

    @classmethod
    def from_dict_of_names_and_filepaths(cls, filepath_name_dict: dict, figure_name: str=None):
        """

        :param filepath_name_dict: dictionary where keys are names of subfigures and values
                                   are the filepaths to the images for those figures.
        :param figure_name: name for overall figure
        :return: Figure
        """
        subfigures = []
        for name, filepath in filepath_name_dict.items():
            subfigures.append(
                Subfigure(filepath, caption=name)
            )

        return cls(subfigures, caption=figure_name)

    def _remove_subfigure_elevate_contents_to_figure_if_single_subfigure(self):
        """
        If there is a single subfigure, leaving in subfigure format results in very small output. Must strip
        out subfigure layer, leaving only a figure with a graphic, then it can fill the page.
        :return:
        """
        if len(self.subfigures) != 1:
            return

        self.subfigures: List[Subfigure]
        # update width to whole page
        graphic = Graphic(self.subfigures[0].graphic.filepath, width=r'1.26\paperwidth')
        # need to turn off centering to cover whole page
        self.centering = False

        self.subfigures = [graphic]



