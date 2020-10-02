from typing import Sequence

from pyexlatex.logic.output.api.builders.base import BaseBuilder


class HTLatexBuilder(BaseBuilder):
    """A simple htlatex-based builder for LaTeX files to generate HTML from LaTeX.

    Builds LaTeX files by copying them to a temporary directly and running
    ``htlatex`` until the associated ``.aux`` file stops changing.

    :param executable: The path to the ``htlatex`` binary (will looked up on
                    ``$PATH``).
    :param max_runs: An integer providing an upper limit on the amount of times
                     ``htlatex`` can be rerun before an exception is thrown.
    """
    output_extension = 'html'
    default_executable = 'htlatex'
    pre_file_output_args: Sequence[str] = tuple()
    post_file_output_args = ('"html,css-in"',)
