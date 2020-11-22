from typing import Optional, Any
from pyexlatex.models.item import Item
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.lists.item import ListItem
from pyexlatex.models.format.nopagebreak import NoPageBreak


class Employment(ContainerItem, Item):
    name = 'employment'

    def __init__(self, contents, company_name: str, employed_dates: str, job_title: str, location: str,
                 extra_contents: Optional[Any] = None, prevent_page_break: bool = True):
        self.company_name = company_name
        self.employed_dates = employed_dates
        self.job_title = job_title
        self.location = location
        self.extra_contents = extra_contents
        self.prevent_page_break = prevent_page_break

        self.add_data_from_content([
            contents,
            company_name,
            employed_dates,
            job_title,
            location,
            extra_contents
        ])

        if not isinstance(contents, (list, tuple)):
            contents = [contents]

        contents = [ListItem(content) for content in contents]

        if extra_contents is not None:
            contents.append(extra_contents)

        kwargs = dict(
            env_modifiers=self._modifier_str,
        )
        if self.prevent_page_break:
            kwargs.update(
                pre_env_contents=NoPageBreak('').env._begin,
                post_env_contents=NoPageBreak('').env._end,
            )

        super().__init__(
            self.name,
            contents,
            **kwargs
        )

    @property
    def _modifier_str(self) -> str:
        output = ''
        for item in [self.company_name, self.employed_dates, self.job_title, self.location]:
            output += self._wrap_with_braces(item)
        return output
