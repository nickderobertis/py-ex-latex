

def format_contents(contents) -> str:
    from dero.latex.logic.builder import _build
    if isinstance(contents, (list, tuple)):
        return _build([_format_content(c) for c in contents])

    return _format_content(contents)


def _format_content(content) -> str:
    from dero.latex.texgen.replacements.file import general_latex_replacements
    return general_latex_replacements(str(content))
