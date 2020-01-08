from copy import deepcopy


def format_contents(contents) -> str:
    from pyexlatex.logic.builder import _build, build

    if isinstance(contents, (list, tuple)):
        contents = [_format_content(c) for c in contents]
        contents = deepcopy(contents)
        contents = build(contents)
        return contents

    return _format_content(contents)


def _format_content(content) -> str:
    from pyexlatex.texgen.replacements.file import general_latex_replacements
    if isinstance(content, str):
        return general_latex_replacements(str(content))
    else:
        # Class is responsible for formatting. This may be a latex class or some
        # other harmless conversion such as int. It may also be an issue if the __str__
        # method of the class is not valid latex
        return content
