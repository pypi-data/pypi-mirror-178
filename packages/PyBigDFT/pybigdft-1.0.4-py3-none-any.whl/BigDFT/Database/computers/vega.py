import yaml
from BigDFT.RemoteRunnerUtils import CallableAttrDict
from BigDFT.URL import URL

meluxina_spec = """
jobname: NAME
mpi: MPI
omp: OMP
time: TIME
submitter: sbatch
project: d2021-135+
qos: default
"""

# this version seems slightly unstable on the frontend for a generic MPI
foss_cuda_openblas = """
prefix: /ceph/hpc/home/eugenovesel/binaries/foss/install
modules:
    - Ninja/1.10.1-GCCcore-10.2.0
    - git/2.28.0-GCCcore-10.2.0-nodocs
    - CMake/3.18.4-GCCcore-10.2.0
    - Boost/1.74.0-GCC-10.2.0
    - Python/3.8.6-GCCcore-10.2.0
    - Eigen/3.3.8-GCCcore-10.2.0
    - Doxygen/1.8.20-GCCcore-10.2.0
    - GSL/2.6-GCC-10.2.0
    - libyaml/0.2.5-GCCcore-10.2.0
    - PyYAML/5.3.1-GCCcore-10.2.0
    - Meson/0.55.3-GCCcore-10.2.0
    - HDF5/1.10.7-gompic-2020b
    - ASE/3.22.0-foss-2020b
    - fosscuda/2020b
    - OpenBLAS/0.3.12-GCC-10.2.0
rcfile: vega-foss.rc
"""

# this version seems slightly unstable on the frontend for a generic MPI
foss_cuda_mkl = """
prefix: /ceph/hpc/home/eugenovesel/binaries/foss-mkl/install
modules:
    - Ninja/1.10.1-GCCcore-10.2.0
    - git/2.28.0-GCCcore-10.2.0-nodocs
    - CMake/3.18.4-GCCcore-10.2.0
    - Boost/1.74.0-GCC-10.2.0
    - Python/3.8.6-GCCcore-10.2.0
    - Eigen/3.3.8-GCCcore-10.2.0
    - Doxygen/1.8.20-GCCcore-10.2.0
    - GSL/2.6-GCC-10.2.0
    - libyaml/0.2.5-GCCcore-10.2.0
    - PyYAML/5.3.1-GCCcore-10.2.0
    - Meson/0.55.3-GCCcore-10.2.0
    - HDF5/1.10.7-gompic-2020b
    - ASE/3.22.0-foss-2020b
    - fosscuda/2020b
    - MKL/mkl_2019.4.243
rcfile: vega-foss-mkl.rc
"""


foss_cuda_standalone = """
prefix: /ceph/hpc/data/d2021-135-users/softwares/BigDFT/binaries-cuda/install
modules:
    - SciPy-bundle/2020.03-foss-2020a-Python-3.8.2
    - fosscuda
    - MKL
    - CMake/3.18.4-GCCcore-10.2.0
    - Meson/0.55.3-GCCcore-10.2.0
    - GSL/2.6-GCC-10.2.0
    - Doxygen/1.8.20-GCCcore-10.2.0
rcfile: vega-foss-cuda.rc
"""

intel = """
prefix: /ceph/hpc/data/d2021-135-users/softwares/BigDFT/binaries/install
modules:
    - SciPy-bundle/2022.05-intel-2022a
    - CMake/3.23.1-GCCcore-11.3.0
    - Meson/0.62.1-GCCcore-11.3.0
rcfile: vega-intel.rc
"""

sources = """
sourcedir: /ceph/hpc/data/d2021-135-users/softwares/BigDFT/sources
package: bigdft
action: build
use_installer: Yes
"""

cpu_account = """
cores_per_node: 256
partition: cpu
"""

gpu_account = """
cores_per_node: 128
gpus_per_node: 4
partition: gpu
"""


class VEGAScriptPrologue(CallableAttrDict):
    def __str__(self):
        shebang = "#!/bin/bash -l"
        pragma = "#SBATCH"
        nodes = self.get('nodes',
                         int((self.mpi*self.omp-1)/self.cores_per_node)+1)
        if 'gpus_per_node' in self:
            gpus = min(self.gpus_per_node*nodes, self.mpi)
        options = [('-J', self.jobname),
                   ('-n', self.mpi),
                   ('-N', nodes),
                   ('-c', self.omp),
                   ('-t', self.time),
                   ('-p', self.partition),
                   ('-o', str(self.jobname)+'.o'),
                   ('-e', str(self.jobname)+'.e'),
                   # ('-A', self.project),
                   # ('-q', self.qos)
                   ]
        if self.partition == 'gpu':
            options.append(('--gres', 'gpu:' + str(gpus)))
        prologue = '\n'.join([shebang] +
                             [' '.join([pragma, opt, str(val)])
                              for opt, val in options])
        return prologue


def base_environment(spec):
    text = '\n'.join(['export PREFIX='+str(spec.prefix)] +
                     (['module purge']
                      if spec.get('purge_modules', True) else []) +
                     ['module load '+str(mod) for mod in spec.modules])
    return text


def machine_epilogue(spec, extra=''):
    text = base_environment(spec)
    text += """
source $PREFIX/bin/bigdftvars.sh
export OMPI_MCA_orte_base_help_aggregate=0
#export OMPI_MCA_coll="^ghc,tuned"
#export MKL_DEBUG_CPU_TYPE=5
export BIGDFT_MPIRUN=mpirun
export FUTILE_PROFILING_DEPTH=0
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
"""
    return '\n'.join((text, extra))


class VegaScript(CallableAttrDict):
    def __str__(self):
        prologue = VEGAScriptPrologue(self)
        epilogue = machine_epilogue(self)
        return '\n'.join([prologue(), epilogue])


class CompileCodeScript(CallableAttrDict):
    def __str__(self):
        from os.path import join
        environment = base_environment(self)
        python = self.get('python', 'python3')
        if self.get('use_installer', False):
            builder = join(self.sourcedir, 'Installer.py -y')
        else:
            builder = join(self.sourcedir, 'bundler', 'jhbuild.py')
        rcfile = '-f '+self.rcfile if 'rcfile' in self else ''
        commands = '\n'.join(
            ['mkdir -p $PREFIX/../ && cd $PREFIX/../',
             'export BIGDFT_SUITE_CHECKOUTROOT=' +
             '/ceph/hpc/data/d2021-135-users/softwares/BigDFT/extra-packages',
             ' '.join([python, builder, rcfile, self.action, self.package,
                      '1>stdout', '2>stderr']), 'cd -'
             ]
            )
        return '\n'.join([environment, commands])


# foss_cuda_openblas =
# foss_cuda_standalone =
# foss_cuda_mkl =

intel_spec = meluxina_spec + intel + cpu_account
foss_cuda_spec = meluxina_spec + foss_cuda_standalone + gpu_account
foss_spec = meluxina_spec + foss_cuda_standalone + cpu_account

submission_script_intel = VegaScript(yaml.load(intel_spec, Loader=yaml.Loader))

submission_script_foss_cuda = VegaScript(yaml.load(foss_cuda_spec,
                                                   Loader=yaml.Loader))

submission_script_foss = VegaScript(yaml.load(foss_spec, Loader=yaml.Loader))


url = URL(host='vega')
