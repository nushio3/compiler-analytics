#!/usr/bin/env python

import src.benchmark
from src.util import *
from src.benchmarks.hello import *

b = HelloBenchmark()
b.generate_program()

system('rsync -avz experiment/ nushio@greatwave.riken.jp:~/experiment/')
system("ssh nushio@greatwave.riken.jp 'cd {dir}; ./compile.sh'".format(dir = b.program_directory()))
stdout_str, _ = system_communicate("ssh nushio@greatwave.riken.jp 'cd {dir}; pjsub ./submit.sh'".format(dir = b.program_directory()))
print "GOT jobname;" +  stdout_str
