from subprocess import Popen
import os

def start_stream(path):
    p = Popen(['export', 'LD_LIBRARY_PATH=.' ], shell=True, cwd=path)
    p = Popen(['sudo chmod 777 ./www'], shell=True, cwd=path)
    p = Popen(['sudo chmod 777 ./www/*'], shell=True, cwd=path)
    p = Popen(['./' + 'mjpg_streamer', '-o', '"output_http.so -w ./www"', '-i', 'input_raspicam.so'], shell=True, cwd=path)

    return p

def end_stream(proc):
    proc.terminate()

