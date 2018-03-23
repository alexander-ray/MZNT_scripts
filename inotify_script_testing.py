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
    
    path_dict = {}
    while True:
        '''
        Names are in the following format:
        IF.1.bin, IF.2.bin, ...
        '''
        prev_key = ''
        # And see the corresponding events:
        for event in inotify.read():
            name = event.name
            # Split name on both periods and underscores
            name_list = re.split(r'[._]+', name)
            # Simple sanity check
            if 'IF' not in name_list[0]:
                continue

            # key is filename, without extension & pre/post
            key = name_list[0] + '_' + name_list[1] + '_' + name_list[2]
            if key not in path_dict:
                path_dict[key] = []
                path_dict[key].append(name)
                if prev_key != '':
                    # Dir name is node_data.*
                    dir_name = prev_key
                    subpath = mz_dir + dir_name
                    os.system('mkdir ' + subpath)
                   
                    # Move all files with this naming convention into new directory
                    # mv should be atomic
                    for f in path_dict[prev_key]:
                        os.system('mv ' + mz_dir + f + ' ' + subpath)
                    
                    # cp scripts into new directory
                    os.system('cp testing_pipeline.sh ' + subpath + '/test.sh')
                    #os.system('cp concatfiles.sh ./' +  subpath + '/concatfiles.sh')
                    os.system('cp unpacker ./' + subpath + '/unpacker')
                    
                    # Code to call shell script with command line arguments
                    subprocess.Popen('./test.sh ' + key + ' ' + sys.argv[1] + ' ' +  sys.argv[2], shell=True, cwd=subpath)

def main():
    # Simple arg check
    if len(sys.argv) <= 2:
        print("Pass path to matlab executable and path to SDR code")
        exit(1)
    subdirs = []
    subdirs.append('./1b81_test/')
    threads = []
    for d in subdirs:
        t = threading.Thread(target=worker, args=(d,))
        threads.append(t)
        t.start()


if __name__ == '__main__':
    main()
