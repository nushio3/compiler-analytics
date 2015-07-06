import subprocess

def system(cmd):
    subprocess.call(cmd, shell=True)


def system_communicate(cmd,input_str = ""):
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return pipe.communicate(input_str)
