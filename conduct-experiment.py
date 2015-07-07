#!/usr/bin/env python

import yaml
import os.path as path

from src.benchmark import *
from src.util import *
from src.benchmarks.simd import *


job_dict = {}
job_state_filename = 'job_state.yaml'

if path.exists(job_state_filename):
    with open(job_state_filename, "r") as fp:
        job_dict=yaml.load(fp)

system('mkdir -p experiment/')
pjstat_output, _ = system_communicate('ssh nushio@greatwave.riken.jp pjstat')
system('rsync -az nushio@greatwave.riken.jp:~/experiment/ experiment/')

running_jobids = []

after_jobid_symbol=False
for l in pjstat_output.split('\n'):
    ws = l.split()
    if ws != []: print ws[0]
    if after_jobid_symbol:
        if len(ws)>=1 : running_jobids.append(ws[0])
    if 'JOB_ID' in ws:
        after_jobid_symbol=True

print running_jobids


for tpow in range(20,30):
    t = 2**tpow
    for n in [4,8,16,32,128,24,48,96]:
        b = SimdBenchmark(problem_size=n, max_time=t)
        b.generate_program()
        key = b.program_filename()
        if key not in job_dict:
            job_dict[key]=b

new_dict={}

for key,job in job_dict.iteritems():
    print job.job_state, key

    st0 = job.job_state
    dir0 = job.program_directory()

    if st0 == JobState.initialized:
        job.generate_program()
        job.job_state = JobState.generated
    elif st0 == JobState.generated:
        system("ssh nushio@greatwave.riken.jp 'cd {dir}; ./compile.sh'".format(dir = dir0))
        pjsub_str, pjsub_err = system_communicate("ssh nushio@greatwave.riken.jp 'cd {dir}; pjsub ./submit.sh'".format(dir = dir0))
        print pjsub_str
        print pjsub_err

        ws = pjsub_str.split()
        job.job_state = JobState.submitted
        job.job_id = ws[ws.index('Job')+1]
    elif st0 == JobState.submitted:
        if job.job_id not in running_jobids: job.job_state = JobState.executed
    elif st0 == JobState.executed:
        system("ssh nushio@greatwave.riken.jp 'cd {dir}; ./analyze.sh'".format(dir = dir0))
        job.job_state = 'analyzed'

    new_dict[key] = job

with open('job_state.yaml', "w") as fp:
    yaml.dump(new_dict,fp)


system('rsync -az experiment/ nushio@greatwave.riken.jp:~/experiment/')




"""
sample format of pjstat


Every 10.0s: pjstat                                                                                  Tue Jul  7 13:42:48 2015


  ACCEPT QUEUED  STGIN  READY RUNING RUNOUT STGOUT   HOLD  ERROR   TOTAL
       0      1      0      0	   0	  0	 0	0      0       1
s      0      1      0      0	   0	  0	 0	0      0       1

JOB_ID     JOB_NAME   MD ST  USER     START_DATE      ELAPSE_LIM NODE_REQUIRE    VNODE  CORE V_MEM
301095     submit.sh  NM QUE nushio   -               0001:00:00 1               -	-    -

"""
