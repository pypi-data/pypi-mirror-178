from BigDFT.RemoteRunnerUtils import CallableAttrDict
from BigDFT.URL import URL

class SpringScript(CallableAttrDict):
    """
    The spring cluster of nodes belonging to the computational molecular
    science research team.
    """
    def __init__(self):
        self.queue = "winter2"
        self.mpi = 1
        self.omp = 36
        self.submitter = "qsub"
        self.prefix = "/home/dawson/binaries/bdft/install"
        self.environment = "remote"
        self.scratch = "/src/dawson"

    def __str__(self):        
        top = "#!/bin/sh\n"
        top += "#PBS -S /bin/bash\n"
        top += "#PBS -q " + self.queue + "\n"
        
        if self.queue in ["winter1", "winter2"]:
            top += "#PBS -l nodes=1:ncpus=36\n"
        elif self.queue in ["winter3"]:
            top += "#PBS -l nodes=1:ncpus=44\n"
        
        middle = "cd $PBS_O_WORKDIR\n"
        middle += "export OMP_NUM_THREADS=" + str(self.omp) + "\n"
        middle += "export PSI_SCRATCH=" + self.scratch + "\n"
        middle += "eval \"$(conda shell.bash hook)\"\n"
        middle += "conda activate " + self.environment + "\n"
        middle += "source " + self.prefix + "/bin/bigdftvars.sh\n"
        
        bottom = "export BIGDFT_MPIRUN=\"mpiexec.hydra -machinefile " + \
                 "$PBS_NODEFILE -n " + str(self.mpi) + \
                 " -perhost " + str(self.mpi) + "\""
        
        return top + middle + bottom
    

submission_script = SpringScript()
url = URL(host="spring.r-ccs27.riken.jp", user="dawson")
