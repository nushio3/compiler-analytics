from util import *

class Benchmark(object):
    def __init__(self):
        0

    def generate_program(self):
        fn = self.program_filename()
        dirn = '/'.join(fn.split('/')[0:-1])

        system('mkdir -p ' + dirn)
        with open(fn, "w") as fp:
            fp.write(self.program_content())
