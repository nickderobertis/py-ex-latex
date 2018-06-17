from dero.latex.figure.models.subfigure import Subfigure
from dero.latex.models import Item
from dero.latex.models.caption import Caption
from dero.latex.models.label import Label
from dero.latex.logic.builder import build_figure_content
from dero.latex.models.document import Document

class Figure(Item):
    name = 'figure'

    def __init__(self, subfigures: [Subfigure], caption=None, label=None, centering=True, position_str=None):
        self.subfigures = subfigures
        self.caption = Caption(caption) if caption else None
        self.label = Label(label) if label else None

        content = build_figure_content(
            self.subfigures,
            caption=self.caption,
            label=self.label,
            centering=centering,
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

    def as_document(self):
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

        return Document(packages, self)

    def to_pdf_and_move(self, as_document=True, outfolder: str=None, outname: str=None):
        from dero.latex.logic.pdf import _document_to_pdf_and_move

        to_output: Figure = self
        if as_document:
            to_output: Document = self.as_document()

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
        return [subfigure.graphic.filepath for subfigure in self]

    @property
    def source_paths(self):
        return [subfigure.graphic.source_path for subfigure in self]

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

