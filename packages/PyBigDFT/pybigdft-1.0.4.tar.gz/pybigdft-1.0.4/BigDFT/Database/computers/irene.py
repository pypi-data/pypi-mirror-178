import yaml
from BigDFT.RemoteRunnerUtils import CallableAttrDict
from BigDFT.URL import URL

ccrt_spec = """
jobname: NAME
mpi: MPI
omp: OMP
time: TIME
filesystem: work,scratch
submitter: ccc_msub
"""

intel_cuda = """
prefix: /ccc/work/cont003/drf/genovesl/binaries/cuda-intel/install
modules:
   - intel/20.0.4
   - mpi/openmpi/4.1.1
   - flavor/cuda/nvhpc-219
   - cuda/11.4
   - python3/3.8.10
"""

sources = """
sourcedir: $HOME/1.9.0
package: bigdft
action: build
"""

sources193 = """
sourcedir: /ccc/work/cont003/drf/genovesl/bigdft-suite
package: bigdft
action: build
use_installer: Yes
rcfile: irene.rc
"""

intel_irene = """
prefix: /ccc/work/cont003/drf/genovesl/binaries/bigdft-1.9.3/install
modules:
    - intel
    - mpi/openmpi/4.0.5
    - mkl
    - python3/3.8.10
    - cmake/3.18.1
    - hdf5/1.8.20
    - boost/1.74.0
"""

gnu_irene = """
prefix: /ccc/work/cont003/drf/genovesl/binaries/bigdft-gnu-1.9.3/install
modules:
   - gnu/8.3.0
   - mpi/openmpi/4.0.2
   - mkl
   - python3/3.8.10
   - cmake/3.18.1
   - hdf5/1.8.20
"""


gnu_cpu = """
prefix: /ccc/work/cont003/drf/genovesl/binaries/gnu8-python3/install
modules:
   - gnu/8.3.0
   - mpi/openmpi/4.0.2
   - mkl
   - intelpython3
   - cmake
"""

irene_account = """
cores_per_node: 128
project: gen12049
queue: rome
"""

topaze_account = """
cores_per_node: 128
queue: a100
"""

irene_spec = """
jobname: NAME
mpi: MPI
omp: OMP
cores_per_node: 128
time: TIME
project: gen12049
filesystem: work,scratch
queue: rome
prefix: /ccc/work/cont003/drf/genovesl/binaries/gnu8-python3/install
modules:
   - gnu/8.3.0
   - mpi/openmpi/4.0.2
   - mkl
   - intelpython3
   - cmake
submitter: ccc_msub
"""

topaze_spec = ccrt_spec + intel_cuda + topaze_account
irene_intel_spec = ccrt_spec + intel_irene + irene_account
irene_gnu_spec = ccrt_spec + gnu_irene + irene_account


class CCRTScriptPrologue(CallableAttrDict):
    def __str__(self):
        shebang = "#!/bin/bash"
        pragma = "#MSUB"
        options = [('-r', self.jobname),
                   ('-N', self.mpi),
                   ('-c', self.omp),
                   ('-T', self.time),
                   ('-q', self.queue),
                   ('-o', 'job-'+str(self.jobname)+'.o'),
                   ('-e', 'job-'+str(self.jobname)+'.e'),
                   ('-m', self.filesystem)]
        if 'project' in self:
            options.append(('-A', self.project))
        prologue = '\n'.join([shebang] +
                             [' '.join([pragma, opt, str(val)])
                              for opt, val in options] +
                             ['set -x', "cd $BRIDGE_MSUB_PWD"])
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
export OMPI_MCA_coll="^ghc,tuned"
export MKL_DEBUG_CPU_TYPE=5
export BIGDFT_MPIRUN='ccc_mprun'
export FUTILE_PROFILING_DEPTH=0
"""
    return '\n'.join((text, 'export OMP_NUM_THREADS='+str(spec.omp), extra))


class IreneScript(CallableAttrDict):
    def __str__(self):
        prologue = CCRTScriptPrologue(self)
        text = '\n'.join(['export PREFIX='+str(self.prefix)] +
                         (['module purge']
                          if self.get('purge_modules', True) else []) +
                         ['module load '+str(mod) for mod in self.modules] +
                         ['export OMP_NUM_THREADS='+str(self.omp)])
        text += """
source $PREFIX/bin/bigdftvars.sh
export PYTHONPATH=$PREFIX/lib/python3.6/site-packages:$PYTHONPATH
export OMPI_MCA_orte_base_help_aggregate=0
export OMPI_MCA_coll="^ghc,tuned"
export MKL_DEBUG_CPU_TYPE=5
export BIGDFT_MPIRUN='ccc_mprun'
export FUTILE_PROFILING_DEPTH=0
"""
        return '\n'.join([prologue(), text])


class IreneScriptNew(CallableAttrDict):
    def __str__(self):
        prologue = CCRTScriptPrologue(self)
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
            ['mkdir $PREFIX/../ && cd $PREFIX/../',
             ' '.join([python, builder, rcfile, self.action, self.package,
                      '1>stdout', '2>stderr']), 'cd -'
             ]
            )
        return '\n'.join([environment, commands])


submission_script = IreneScript(yaml.load(irene_spec, Loader=yaml.Loader))

submission_script_new = IreneScriptNew(yaml.load(topaze_spec,
                                                 Loader=yaml.Loader))

compilation_commands = CompileCodeScript(yaml.load(sources + gnu_cpu,
                                                   Loader=yaml.Loader))

submission_script_intel = IreneScriptNew(yaml.load(irene_intel_spec,
                                                   Loader=yaml.Loader))

submission_script_gnu = IreneScriptNew(yaml.load(irene_gnu_spec,
                                                 Loader=yaml.Loader))


url = URL(host='irene')

url_topaze = URL(host='topaze')
