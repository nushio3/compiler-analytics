from util import *
import enum

class JobState(str, enum.Enum):
    initialized = 'initialized'
    generated = 'generated'
    submitted = 'submitted'
    executed = 'executed'
    analyzed = 'analyzed'

class Benchmark(object):
    def __init__(self):
        self.job_state = JobState.initialized
        self.job_id = ''

    def program_directory(self):
        return '/'.join(self.program_filename().split('/')[0:-1])
    def program_filename_body(self):
        return self.program_filename().split('/')[-1].split('.')[0]

    def generate_program(self):
        fn = self.program_filename()
        dirn = self.program_directory()
        subfn = dirn + "/submit.sh"
        cmpfn = dirn + "/compile.sh"
        analfn = dirn + "/analyze.sh"

        system('mkdir -p ' + dirn)
        with open(fn, "w") as fp:
            fp.write(self.program_content())
        with open(subfn, "w") as fp:
            fp.write(self.submit_script_content())
        with open(cmpfn, "w") as fp:
            fp.write(self.compile_script_content())
        with open(analfn, "w") as fp:
            fp.write(self.postprocess_script_content())
        system('chmod 755 ' + subfn)
        system('chmod 755 ' + cmpfn)
        system('chmod 755 ' + analfn)

    def compile_script_content(self):
        return """
module load sparc
FCCpx -Kfast,openmp,parallel,ocl,unroll,optmsg=2,restp=all  -Nsrc,sta,lst=t {fn}.cpp -S
FCCpx -Kfast,openmp,parallel,ocl {fn}.s -o {fn}.out
""".format(fn=self.program_filename_body())


    def submit_script_content(self):
        return """
#!/bin/sh
#PJM -L rscunit=gwmpc
#PJM -L node=1
#PJM -L elapse=1:00:00
#PJM -j

rm pi.0 -fr
rm pa.? -fr
rm pa.?? -fr

export OMP_NUM_THREADS=32
fipp -Srange -C -Ihwm -d pi.0  ./{fn}.out
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


    def postprocess_script_content(self):
        return """
module load sparc
mkdir -p prof
fipppx -A -Icpu,hwm -d pi.0 -o   prof/simple.txt
fapppx -A -p all -l0 -d pa.1 -o  prof/output_1.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.2 -o  prof/output_2.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.3 -o  prof/output_3.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.4 -o  prof/output_4.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.5 -o  prof/output_5.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.6 -o  prof/output_6.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.7 -o  prof/output_7.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.8 -o  prof/output_8.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.9 -o  prof/output_9.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.10 -o prof/output_10.csv -tcsv -Hpa
fapppx -A -p all -l0 -d pa.11 -o prof/output_11.csv -tcsv -Hpa
"""
