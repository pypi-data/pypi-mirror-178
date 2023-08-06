import os
import math
import yaml
import logging
from BigDFT.RemoteRunnerUtils import CallableAttrDict
from BigDFT.URL import URL

# create and link logger
module_logger = logging.getLogger(__name__)
# some long string that won't be accidentally entered
filler = 'summerscript_defaultvalue'
summer_spec = f"""
name: {filler}
mpi: {filler}
omp: {filler}
nodes: {filler}
time: {filler}
# project: {filler}
queue: short
sourcepath: {filler}
modules:
   - icc
   - impi
   - mkl/18
   - python/anaconda3
submitter: qsub
max_per_node: 32
omp_thread_limit: -1  # set +ve to limit the OMP threading
extra_lines: []
mpi_command_line: ''
check_resources: False
"""


def safe_divide(a, b):
    """
    always-fit division. Rounds up after division, always returns >= 1
    """
    r = math.ceil(a / b)
    return max(r, 1)


class SummerScriptPrologue(CallableAttrDict):
    def __str__(self):

        max_per_node_lim = 40

        if self.max_per_node > max_per_node_lim:
            raise ValueError('max_per_node is greater than the number '
                             'of physical cores available '
                             f'({max_per_node_lim})')

        if self.nodes == filler:
            nodes = safe_divide(self.mpi, self.max_per_node)
        else:
            nodes = self.nodes
        # omp = self.omp
        self.tpn = safe_divide(self.mpi, nodes)

        lims = {'standard': (4, None),
                'mono': (1, 1),
                'short': (32, 512),
                'csp': (32, 1024)}

        # TODO check actual values of limits
        if self.queue in lims and self.check_resources:
            nodemin = lims[self.queue][0]
            nodemax = lims[self.queue][1]

            processes = nodes * self.mpi

            if processes < nodemin:
                raise ValueError(f'{processes} processes is too low for '
                                 f'queue {self.queue} (min {nodemin})')

            if nodemax and processes > nodemax:
                raise ValueError(f'{processes} processes is too high for '
                                 f'queue {self.queue} (max {nodemax})')

        shebang = "#!/bin/bash"
        pragma = "#PBS"
        options = [('-N', self.name),
                   ('-q', self.queue),
                   ('-o', f'{self.name}-stdout'),
                   ('-e', f'{self.name}-stderr'),]
        resources = f'#PBS -l nodes={nodes}:' \
                    f'ppn={self.mpi},' \
                    f'walltime={self.time}'
        prologue = '\n'.join([shebang] +
                             [f'{pragma} {opt} {str(val)}'
                              for opt, val in options] +
                             [resources])
        return prologue + '\n'


class SummerScript(CallableAttrDict):

    def __str__(self):
        tlim = self.omp_thread_limit
        threads = tlim if tlim > 0 else self.omp
        prologue = SummerScriptPrologue(self)

        # these parameters can be ignored, and filled automatically
        # for validation
        self.can_be_default = ['nodes',
                               'sourcepath']

        if self.sourcepath == filler:
            # sourcepath = '/W/$USER/build/install/bin/bigdftvars.sh'
            sourcepath = '/W/$USER/build/bigdft/bigdftvars.sh'
        else:
            sourcepath = self.sourcepath

        text = ''
        run = 'qsub'

        text += '\n'.join(['module load ' + str(mod) for mod in self.modules])
        text += '\n\ncd $PBS_O_WORKDIR'
        text += f'\n\nexport OMP_NUM_THREADS={threads}'

        text += f"""
\nsource {sourcepath}
export BIGDFT_MPIRUN='mpirun'
export FUTILE_PROFILING_DEPTH=0
"""
        for line in self.extra_lines:
            text += line
        return '\n'.join([prologue(), text])

    @property
    def missing(self):
        """
        return non-updated arguments
        """
        self.__str__()
        missing = [k for k, v in self.items() if v == str(filler) and k not in self.can_be_default]
        module_logger.debug(f'missing arguments: {missing}')
        return missing

    @property
    def valid(self):
        valid = len(self.missing) == 0
        module_logger.debug(f'checking if script is valid: {valid}')
        return valid


submission_script = SummerScript(yaml.load(summer_spec, Loader=yaml.Loader))
url = URL()
