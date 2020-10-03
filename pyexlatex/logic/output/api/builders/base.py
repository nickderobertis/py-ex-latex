import os
import subprocess
from subprocess import CalledProcessError
from typing import Optional, List, Sequence

from future.utils import raise_from
from data import Data as I
from data.decorators import data
from shutilwhich import which
from tempdir import TempDir

from latex.exc import LatexBuildError


class BaseBuilder:
    """
    The base class for LaTeX file builders
    """
    output_extension: str
    pre_file_output_args: Sequence[str] = (
        '-interaction=batchmode',
        '-halt-on-error',
        '-shell-escape',
        '-file-line-error'
    )
    post_file_output_args: Sequence[str] = tuple()
    default_executable: str

    def __init__(self, executable: Optional[str] = None, bibtex: str = 'bibtex', max_runs: int = 15):
        if executable is None:
            executable = self.default_executable

        self.executable = executable
        self.bibtex = bibtex
        self.max_runs = max_runs

    @data('source')
    def build(self, source, texinputs: Optional[List[str]] = None, run_bibtex: bool = False):
        if texinputs is None:
            texinputs = []

        with TempDir() as tmpdir,\
                source.temp_saved(suffix='.latex', dir=tmpdir) as tmp:
            # close temp file, so other processes can access it also on Windows
            tmp.close()
            called_bibtex = False

            # calculate output filename
            base_fn = os.path.splitext(tmp.name)[0]
            output_fn = base_fn + f'.{self.output_extension}'
            aux_fn = base_fn + '.aux'
            args = [self.executable, *self.pre_file_output_args, tmp.name, *self.post_file_output_args]

            # create environment
            newenv = os.environ.copy()
            inputs_value = os.pathsep.join(texinputs) + os.pathsep
            newenv['TEXINPUTS'] = inputs_value
            newenv['BSTINPUTS'] = inputs_value

            # run until aux file settles
            prev_aux = None
            runs_left = self.max_runs
            self._pre_compile(tmpdir, base_fn)
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
                            # TODO [#9]: better handling for LaTeX exceptions
                            #
                            # Parse log file, raise proper exception
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
        return bool(which(self.executable))

    def _pre_compile(self, temp_dir: str, base_file_name: str):
        pass
