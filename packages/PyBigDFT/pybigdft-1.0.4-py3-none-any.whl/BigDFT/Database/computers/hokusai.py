from BigDFT.RemoteRunnerUtils import CallableAttrDict
from BigDFT.URL import URL

class HokusaiScript(CallableAttrDict):
    """
    The Hokusai Blue Wave supercomputer hosted at RIKEN.
    """
    def __init__(self):
        self.number_of_nodes = 1
        self.mpi = 1
        self.omp = 40
        self.time = "0:10:00"
        self.project = "Q22460"
        self.submitter = "pjsub"
        self.prefix = "/home/wddawson/binaries/bdft/install"
        self.environment = "remote"

    def __str__(self):        
        ppn = int(self.mpi/self.number_of_nodes)
        top = "#!/bin/sh\n"
        top += "#PJM -L rscunit=bwmpc\n"
        top += "#PJM -L rscgrp=batch\n"
        top += "#PJM -L vnode=" + str(self.number_of_nodes) + "\n"
        top += "#PJM -L vnode-core=40\n"
        top += "#PJM -L elapse=" + self.time + "\n"
        top += "#PJM -g " + self.project + "\n"
        top += "#PJM -j\n"
        
        middle = "source ~/.bashrc\n"
        middle += 'export BIGDFT_MPIRUN="mpirun -np ' + \
                  str(self.number_of_nodes*ppn) + \
                  ' -ppn ' + str(ppn) + '"\n'
        middle += "source " + self.prefix + "/bin/bigdftvars.sh\n"
        middle += "export OMP_NUM_THREADS=" + str(self.omp) + "\n"    
        middle += "conda activate " + self.environment + "\n"
        
        return top + middle
    

submission_script = HokusaiScript()
url = URL(host="hokusai.riken.jp")
