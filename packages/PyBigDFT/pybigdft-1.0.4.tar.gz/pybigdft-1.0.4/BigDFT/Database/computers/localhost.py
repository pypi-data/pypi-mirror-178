import yaml
from BigDFT.RemoteRunnerUtils import CallableAttrDict

spec = """
jobname: NAME
mpi: MPI
omp: OMP
time: TIME
bindir: $BIGDFT_ROOT
submitter: bash
append_string: ''
"""

compilation_dict = """
sourcedir: $BIGDFT_SUITE_SOURCES
prefix: $BIGDFT_PREFIX
package: bigdft
action: build
"""


class ScriptPrologue(CallableAttrDict):
    def __str__(self):
        shebang = "#!/bin/bash"
        return shebang + '\n'


class LocalScript(CallableAttrDict):
    def __str__(self):
        prologue = ScriptPrologue(self)
        text = [prologue(),
                'export OMP_NUM_THREADS='+str(self.omp),
                'source '+str(self.bindir)+'/bigdftvars.sh',
                'export FUTILE_PROFILING_DEPTH=0',
                'export BIGDFT_MPIRUN="mpirun -np '+str(self.mpi)+'"',
                self.append_string+'\n']
        return '\n'.join(text)


class CompileCodeScript(CallableAttrDict):
    def __str__(self):
        from os.path import join
        environment = 'export PREFIX='+self.prefix
        python = self.get('python', 'python3')
        if self.get('use_installer', False):
            builder = join(self.sourcedir, 'Installer.py -y')
        else:
            builder = join(self.sourcedir, 'bundler', 'jhbuild.py')
        rcfile = '-f '+self.rcfile if 'rcfile' in self else ''
        commands = '\n'.join(
            ['mkdir -p $PREFIX/../ && cd $PREFIX/../',
             ' '.join([python, builder, rcfile, self.action, self.package,
                      '1>stdout', '2>stderr']),
             'cd -'
             ]
            )
        return '\n'.join([environment, commands])


submission_script = LocalScript(yaml.load(spec, Loader=yaml.Loader))

compilation_commands = CompileCodeScript(yaml.load(compilation_dict,
                                                   Loader=yaml.Loader))
