import time
import os

def follow(thefile):
    for line in thefile.readlines()[-10:]:
        yield line
    thefile.seek(0, os.SEEK_END)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

logfile = open('access-log')
loglines = follow(logfile)

for line in loglines:
    print(line, end='')
