from typing import Optional, Sequence, Union
from pyexlatex.presentation.beamer.frame.frame import Frame
from pyexlatex.models.title.title import Title
from pyexlatex.models.title.subtitle import Subtitle
from pyexlatex.models.credits.author import Author
from pyexlatex.models.date import Date
from pyexlatex.models.title.framepage import MakeFrameTitle


class TitleFrame(Frame):

    def __init__(self, title: Optional[str] = None, authors: Optional[Union[str, Sequence[str]]] = None, date: Optional[str] = None,
                 short_title: Optional[str] = None, subtitle: Optional[str] = None, short_author: Optional[str] = None,
                 institutions: Optional[Sequence[Sequence[str]]] = None, short_institution: Optional[str] = None,
                 **kwargs):
        pre_env_contents = [
            Title(title, short_title=short_title) if title is not None else None,
            Subtitle(subtitle) if subtitle is not None else None,
            Author(
                authors,
                institutions=institutions,
                short_institution=short_institution,
                short_author=short_author
            ) if authors is not None else None,
            Date(date) if date is not None else Date()
        ]

        self.pre_env_content = [content for content in pre_env_contents if content is not None]
        self.add_data_from_content(self.pre_env_content)
        from pyexlatex.logic.builder import _build
        pre_env_contents = _build(self.pre_env_content)

        super().__init__(MakeFrameTitle(), label='title-frame', pre_env_contents=pre_env_contents, **kwargs)


def should_create_title_frame(title: str = None, authors: Optional[Union[str, Sequence[str]]] = None, date: str = None,
                              subtitle: Optional[str] = None, institutions: Optional[Sequence[Sequence[str]]] = None):
    return any([
        title is not None,
        authors is not None,
        date is not None,
        subtitle is not None,
        institutions is not None
    ])