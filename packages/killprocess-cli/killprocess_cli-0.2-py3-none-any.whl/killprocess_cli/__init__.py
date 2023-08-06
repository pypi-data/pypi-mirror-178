import os
import subprocess
import re
import sys

def main():
    output = subprocess.check_output("ps aux | grep "+sys.argv[1], shell=True)
    output = output.decode()
    f = open("data", "w")
    f.write(output)
    f.close()
    f = open('data', 'r')
    Lines = f.readlines()

    process_list = 'kill '

    for line in Lines:
        res = re.sub(' +', ' ', line.strip())
        process_list = process_list + res.split(' ')[1] + ' '
    #os.system(process_list)
    res = subprocess.run(process_list.split(' '), capture_output=True)