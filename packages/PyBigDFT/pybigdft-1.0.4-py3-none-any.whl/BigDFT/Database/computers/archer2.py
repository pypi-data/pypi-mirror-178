import os
import math
import yaml
import logging
from BigDFT.RemoteRunnerUtils import CallableAttrDict
from BigDFT.URL import URL

# create and link logger
module_logger = logging.getLogger(__name__)
# some long string that won't be accidentally entered
filler = 'archer2script_defaultvalue'
archer2_spec = f"""
name: {filler}
mpi: {filler}
omp: {filler}
number_of_nodes: {filler}
time: {filler}
project: {filler}
sourcepath: {filler}
qos: standard
partition: standard
modules:
   - cray-python
   - mkl
submitter: sbatch
max_per_node: 128
omp_thread_limit: -1  # set +ve to limit the OMP threading
extra_lines: []
mpirun_path: /work/e572/e572/shared/openmpi/bin/
mpi_command_line: ''
"""


def safe_divide(a, b):
    """
    always-fit division. Rounds up after division, always returns > 1
    """
    r = math.ceil(a / b)
    return max(r, 1)


class Archer2ScriptPrologue(CallableAttrDict):
    def __str__(self):
        if self.max_per_node > 128:
            raise ValueError('max_per_node is greater than the number '
                             'of physical cores available (128)')

        if self.number_of_nodes == filler:
            nodes = safe_divide(self.omp * self.mpi, self.max_per_node)
        else:
            nodes = self.number_of_nodes
        omp = self.omp
        self.tpn = safe_divide(self.mpi, nodes)

        shebang = "#!/bin/bash"
        pragma = "#SBATCH"
        options = [('--job-name', self.name),
                   ('--nodes', nodes),
                   ('--cpus-per-task', omp),
                   ('--tasks-per-node', self.tpn),
                   ('--time', self.time),
                   ('--account', self.project),
                   ('--qos', self.qos),
                   ('--partition', self.partition),
                   ('--export', 'none')]
        prologue = '\n'.join([shebang] +
                             [f'{pragma} {opt}={str(val)}'
                              for opt, val in options])
        return prologue


class Archer2Script(CallableAttrDict):

    def __str__(self):
        tlim = self.omp_thread_limit
        threads = tlim if tlim > 0 else self.omp
        prologue = Archer2ScriptPrologue(self)

        self.can_be_default = ['nodes',
                               'sourcepath']

        if self.sourcepath == filler:
            sourcepath = f'/work/{self.project}/{self.project}/' \
                         '$USER/build/bigdft/bigdftvars.sh'
        else:
            sourcepath = self.sourcepath

        if self.get('openmpi', False):
            text = "\nmodule swap PrgEnv-cray PrgEnv-gnu\nmodule unload cray-mpich\n"
            run = self.mpirun_path + 'mpirun'

            if self.mpi_command_line != '':
                run += f' {self.mpi_command_line}'

        else:
            text = ''
            run = 'srun --hint=nomultithread --distribution=block:block'

        text += '\n'.join(['module load ' + str(mod) for mod in self.modules])
        text += f'\nexport OMP_NUM_THREADS={threads}'

        text += f"""
source {sourcepath}
export BIGDFT_MPIRUN='{run}'
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


submission_script = Archer2Script(yaml.load(archer2_spec, Loader=yaml.Loader))
openmpi_spec = yaml.safe_load(archer2_spec)
openmpi_spec['openmpi'] = True
openmpi_submission_script = Archer2Script(openmpi_spec)
url = URL()
