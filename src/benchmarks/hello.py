from src.benchmark import *

class HelloBenchmark(Benchmark):
    def __init__ (self):
        0

    def program_filename(self):
        return "experiment/hello_world/main.cpp"

    def program_content(self):
        return """
#include <stdio.h>

int main () {
  printf("hello\\n");
  return 0;
}
"""
