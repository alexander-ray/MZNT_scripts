import os
import sys
import subprocess

# Pip3 install inotify_simple
from inotify_simple import INotify, flags
'''
# Make subdir for IF files
if len(sys.argv) > 1:
    path = "./" + sys.argv[1]
    os.mkdir(path)
else:
    print("Pass base name of IF log files")
    exit(1)
'''

inotify = INotify()
watch_flags = flags.CREATE
wd = inotify.add_watch('./', watch_flags)

# Maintain dictionary of names
# Once I get one, make sure it's "pre" and add to dictionary
# If I have a filename that's been added to dict, double check that it's "post"
# mkdir with base name, move both files in as well as .sh (time?)
# Unpack, concat, run matlab (should all be script)
path_dict = {}

while True:
    # And see the corresponding events:
    for event in inotify.read():
        name_list = event.name.split('.')
        if name_list[0] != 'microzed':
            continue

	# name_list[2] is pre/post
        if name_list[0] in path_dict and name_list[2] == 'post':
            # Dir name is concatenated pre timestamp
            dir_name = path_dict[name_list[0]] + '_' + name_list[0] 

            os.system('mkdir ' + dir_name)
            # Move all files with this naming convention into new directory
            os.system('mv ' + name_list[0] + '* ./' + dir_name)
            # cp shell script into new directory
            os.system('cp testing_pipeline.sh ./' + dir_name)
            # CALL TESTING PIPELINE SCRIPT
        elif name_list[0] not in path_dict and name_list[2] == 'pre':
            path_dict[name_list[0]] = name_list[1]

# Code to call shell script with command line arguments
#subprocess.call(['./test.sh', 'why', 'helloworld'])
