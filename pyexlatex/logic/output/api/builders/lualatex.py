from pyexlatex.logic.output.api.builders.base import BaseBuilder


class LuaLatexBuilder(BaseBuilder):
    """A simple lualatex-based builder for LaTeX files.

    Builds LaTeX files by copying them to a temporary directly and running
    ``lualatex`` until the associated ``.aux`` file stops changing.

    :param executable: The path to the ``lualatex`` binary (will looked up on
                    ``$PATH``).
    :param max_runs: An integer providing an upper limit on the amount of times
                     ``lualatex`` can be rerun before an exception is thrown.
    """
    output_extension = 'pdf'
    default_executable = 'lualatex'

