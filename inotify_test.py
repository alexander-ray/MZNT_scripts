import os
import sys
import time
import subprocess

# Pip3 install inotify_simple
from inotify_simple import INotify, flags


# Make subdir for IF files
if len(sys.argv) > 1:
    path = "./" + sys.argv[1]
    os.mkdir(path)
else:
    print("Pass base name of IF log files")
    exit(1)


inotify = INotify()
watch_flags = flags.CREATE
wd = inotify.add_watch(path, watch_flags)

while True:
    start = time.time()
    # And see the corresponding events:
    for event in inotify.read():
        print(event)
        print(time.time() - start)

# Code to call shell script with command line arguments
#subprocess.call(['./test.sh', 'why', 'helloworld'])
