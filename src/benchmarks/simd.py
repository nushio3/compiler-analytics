from src.benchmark import *
from string import Template

class SimdBenchmark(Benchmark):
    def __init__ (self,problem_size=128, max_time=1073741824):
        Benchmark.__init__(self)
        self.problem_size=problem_size
        self.max_time=max_time

    def program_filename(self):
        ident = '/'.join(['N={}'.format(self.problem_size), 'T={}'.format(self.max_time)])
        return "experiment/hello_simd/" + ident +  "/main.cpp"

    def program_content(self):
        return Template("""
#include <fj_tool/fipp.h>
#include <fjcoll.h>
#include <stdio.h>

const int N = $problem_size ;
const size_t N_TIME = $max_time ;

int main () {
  double a[N],b[N],c[N];

  for (int i=0;i<N;++i) {
    double x=1.0+i;
    a[i]=x; b[i]=1/x/x; c[i]=x*x*x;
  }

  fipp_start();
  start_collection("main_loop");

  asm volatile("#central loop begin");
  for (size_t t=0;t<N_TIME;++t) {
#pragma loop noalias
#pragma loop simd
#pragma loop unroll
    for (int i=0;i<N;++i) {
      a[i]=a[i]*b[i]+c[i];
    }
  }
  asm volatile("#central loop end");

  stop_collection("main_loop");
  fipp_stop();

  for (int i=0;i<N;++i) {
    printf("%lf ",a[i]);
  }
}
""").substitute(problem_size=self.problem_size, max_time=self.max_time)
