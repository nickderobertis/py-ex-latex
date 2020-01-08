import os
import subprocess
from subprocess import CalledProcessError

from future.utils import raise_from
from data import Data as I
from data.decorators import data
from shutilwhich import which
from tempdir import TempDir

from latex.exc import LatexBuildError


class LuaLatexBuilder:
    """A simple lualatex based buidler for LaTeX files.

    Builds LaTeX files by copying them to a temporary directly and running
    ``lualatex`` until the associated ``.aux`` file stops changing.

    .. note:: This may miss changes if ``biblatex`` or other additional tools
              are used. Usually, the :class:`~latex.build.LatexMkBuilder` will
              give more reliable results.

    :param lualatex: The path to the ``pdflatex`` binary (will looked up on
                    ``$PATH``).
    :param max_runs: An integer providing an upper limit on the amount of times
                     ``pdflatex`` can be rerun before an exception is thrown.
    """

    def __init__(self, lualatex='lualatex', bibtex: str = 'bibtex', max_runs=15):
        self.lualatex = lualatex
        self.bibtex = bibtex
        self.max_runs = 15

    @data('source')
    def build_pdf(self, source, texinputs=[], run_bibtex: bool = False):
        with TempDir() as tmpdir,\
                source.temp_saved(suffix='.latex', dir=tmpdir) as tmp:

            # close temp file, so other processes can access it also on Windows
            tmp.close()
            called_bibtex = False

            # calculate output filename
            base_fn = os.path.splitext(tmp.name)[0]
            output_fn = base_fn + '.pdf'
            aux_fn = base_fn + '.aux'
            args = [self.lualatex, '-interaction=batchmode',
                    '-halt-on-error',
                    '-shell-escape', '-file-line-error',
                    tmp.name]

            # create environment
            newenv = os.environ.copy()
            inputs_value = os.pathsep.join(texinputs) + os.pathsep
            newenv['TEXINPUTS'] = inputs_value
            newenv['BSTINPUTS'] = inputs_value

            # run until aux file settles
            prev_aux = None
            runs_left = self.max_runs
            while runs_left:
                try:
                    subprocess.check_call(args,
                                          cwd=tmpdir,
                                          env=newenv,
                                          stdin=open(os.devnull, 'r'),
                                          stdout=open(os.devnull, 'w'), )
                except CalledProcessError as e:
                    raise_from(LatexBuildError(base_fn + '.log'), e)

                # check aux-file
                aux = open(aux_fn, 'rb').read()

                if aux == prev_aux:
                    # Stable aux file
                    if run_bibtex and not called_bibtex:
                        called_bibtex = True  # ensure only called once
                        bibtex_args = [self.bibtex, os.path.basename(aux_fn)]
                        try:
                            subprocess.check_call(bibtex_args,
                                              cwd=tmpdir,
                                              env=newenv,
                                              stdin=open(os.devnull, 'r'),
                                              stdout=open(os.devnull, 'w'), )
                        except CalledProcessError as e:
                            # TODO: parse log file, raise proper exception
                            with open(base_fn + '.blg', 'r') as f:
                                log_contents = f.read()
                            raise Exception(log_contents)
                        continue  # go back into the loop to process with biblography
                    break

                prev_aux = aux
                runs_left -= 1
            else:
                raise RuntimeError(
                    'Maximum number of runs ({}) without a stable .aux file '
                    'reached.'.format(self.max_runs))

            return I(open(output_fn, 'rb').read(), encoding=None)

    def is_available(self):
        return bool(which(self.lualatex))
