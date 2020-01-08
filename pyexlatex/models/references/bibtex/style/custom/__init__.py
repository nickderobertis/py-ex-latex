from pyexlatex.models.references.bibtex.style.custom.jof import jof_style

CUSTOM_STYLES_OBJS = [
    jof_style
]

CUSTOM_STYLES = {style.style_name: style for style in CUSTOM_STYLES_OBJS}
