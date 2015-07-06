from util import *

class Benchmark(object):
    def __init__(self):
        0

    def program_directory(self):
        return '/'.join(self.program_filename().split('/')[0:-1])
    def program_filename_body(self):
        return self.program_filename().split('/')[-1].split('.')[0]

    def generate_program(self):
        fn = self.program_filename()
        dirn = self.program_directory()
        subfn = dirn + "/submit.sh"
        cmpfn = dirn + "/compile.sh"

        system('mkdir -p ' + dirn)
        with open(fn, "w") as fp:
            fp.write(self.program_content())
        with open(subfn, "w") as fp:
            fp.write(self.submit_script_content())
        with open(cmpfn, "w") as fp:
            fp.write(self.compile_script_content())
        system('chmod 755 ' + subfn)
        system('chmod 755 ' + cmpfn)


    def submit_script_content(self):
        return """
#!/bin/sh
#PJM -L rscunit=gwmpc
#PJM -L node=1
#PJM -L elapse=1:00:00
#PJM -j

export OMP_NUM_THREADS=32
fapp -C -d pa.1 -Hpa=1   ./{fn}.out
fapp -C -d pa.2 -Hpa=2   ./{fn}.out
fapp -C -d pa.3 -Hpa=3   ./{fn}.out
fapp -C -d pa.4 -Hpa=4   ./{fn}.out
fapp -C -d pa.5 -Hpa=5   ./{fn}.out
fapp -C -d pa.6 -Hpa=6   ./{fn}.out
fapp -C -d pa.7 -Hpa=7   ./{fn}.out
fapp -C -d pa.8 -Hpa=8   ./{fn}.out
fapp -C -d pa.9 -Hpa=9   ./{fn}.out
fapp -C -d pa.10 -Hpa=10 ./{fn}.out
fapp -C -d pa.11 -Hpa=11 ./{fn}.out
""".format(fn=self.program_filename_body())

    def compile_script_content(self):
        return """
module load sparc
FCCpx -Kfast,openmp,parallel,ocl,optmsg=2  -Nsrc,sta,lst=t {fn}.cpp -S
FCCpx -Kfast,openmp,parallel,ocl {fn}.s -o {fn}.out
""".format(fn=self.program_filename_body())
