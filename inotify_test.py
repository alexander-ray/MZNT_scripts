import os
import sys
import subprocess
import threading
import re
from time import sleep
# Pip3 install inotify_simple
from inotify_simple import INotify, flags

def worker(mz_dir):
    inotify = INotify()
    #watch_flags = flags.CREATE | flags.MODIFY | flags.MOVED_TO
    watch_flags = flags.CREATE
    # Assume directory has been created if thread has spawned
    wd = inotify.add_watch(mz_dir, watch_flags) 
    
    # Once I get one, make sure it's "pre" and add to dictionary
    # If I have a filename that's been added to dict, double check that it's "post"
    # mkdir with base name, move both files in as well as .sh (time?)
    # Unpack, concat, run matlab (should all be script)
    #POST_BYTES = 20000000
    POST_BYTES = 499646464
    # Keys will be mz1_preData.*
    path_dict = {}

    while True:
        '''
        Names are in the following format:
        mz1.IF.bin, mz1.IF.bin.1.bin, mz1.IF.bin.2.bin, etc for periodic IF
        mz1_preData.0.bin and mz1_postData.0.bin for RFI event
             mz1_preData.0.bin.0 and mz1_preData.0.bin.1 for fragmented pre files
        '''
        # And see the corresponding events:
        for event in inotify.read():
            name = event.name
            # Split name on both periods and underscores
            name_list = re.split(r'[._]+', name)
            # Simple sanity check
            if 'Data' not in name_list[1]:
                continue

            # key is filename, without extension & pre/post
            key = name_list[0] + '_' + 'data.' + name_list[2]
            if ((key in path_dict) and ('post' in name)) or
                ((key not in path_dict) and ('pre' not in name) and ('post' not in name)):
                # Dir name is node_data.*
                dir_name = key
                subpath = mz_dir + dir_name
                os.system('mkdir ' + subpath)
               
                # While post hasn't been fully written, sleep
                while os.stat(mz_dir + name).st_size < POST_BYTES:
                    sleep(0.5)
                
                path_dict[key].append(name)
                # Move all files with this naming convention into new directory
                # mv should be atomic
                for f in path_dict[key]:
                    os.system('mv ' + mz_dir + f + ' ' + subpath)
                
                # cp scripts into new directory
                os.system('cp testing_pipeline.sh ' + subpath + '/test.sh')
                os.system('cp concatfiles.sh ./' +  subpath + '/concatfiles.sh')
                os.system('cp unpacker ./' + subpath + '/unpacker')
                
                # Code to call shell script with command line arguments
                subprocess.Popen('./test.sh ' + key + ' ' + sys.argv[1] + ' ' +  sys.argv[2], shell=True, cwd=subpath)
            # another pre file
            elif (key in path_dict) and ('pre' in name):
                path_dict[key].append(name)
            # First pre file, add key to dict, append full filename
            elif key not in path_dict:
                path_dict[key] = []
                path_dict[key].append(name)

def main():
    # Simple arg check
    if len(sys.argv) <= 2:
        print("Pass path to matlab executable and path to SDR code")
        exit(1)
    subdirs = []
    subdirs.append('./mz1/test3/')
    subdirs.append('./mz2/test3/')
    subdirs.append('./mz3/test3/')
    #mz4_t = './mz4/test3/'
    #mz5_t = './mz5/test3/'
    #mz6_t = './mz6/test3/'
    threads = []
    for d in subdirs:
        t = threading.Thread(target=worker, args=(d,))
        threads.append(t)
        t.start()


if __name__ == '__main__':
    main()
