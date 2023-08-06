from BigDFT.RemoteRunnerUtils import CallableAttrDict
from BigDFT.URL import URL


class FugakuScript(CallableAttrDict):
    def __str__(self):
        ppn = int(self.mpi/self.number_of_nodes)

        top = "#!/bin/sh\n"
        top += '#PJM -L "node=' + str(self.number_of_nodes) + '"\n'
        top += '#PJM -L "rscunit=rscunit_ft01"\n'
        if self.number_of_nodes <= 384:
            top += '#PJM -L "rscgrp=small"\n'
        else:
            top += '#PJM -L "rscgrp=large"\n'
        top += '#PJM -L "elapse=' + str(self.time) + '"\n'
        top += '#PJM --mpi "max-proc-per-node=' + str(ppn) + '"\n'

        middle = 'export FUTILE_PROFILING_DEPTH=0\n'
        middle += 'module load Python3-CN\n'
        middle += 'export FLIB_CNTL_BARRIER_ERR=FALSE\n'
        middle += "source " + self.prefix + "/bin/bigdftvars.sh\n"
        middle += 'export BIGDFT_MPIRUN="mpiexec -std ' + \
                  self.jobname + '.txt"\n'
        middle += "export OMP_NUM_THREADS=" + str(self.omp) + "\n"    

        return top + middle

    
submission_script = FugakuScript()
submission_script.prefix = "/home/hp200179/u00771/binaries/bds/install"
submission_script.submitter = "pjsub"

url = URL(host="fugaku.r-ccs.riken.jp")
