#!/bin/bash
# $1 is base name of bin files
# Bin files must be at same level or lower in directory structure
# $2 is path to matlab executable
# $3 is path to SDR code directory

# Directory should be created by inotify script
#mkdir ${1}
mkdir ./${1}/unpacked
touch ./${1}/${1}_log

echo "Combining IF files" >> ./${1}/${1}_log
find . -type f -name "${1}.bin*" -print0 | sort -z | xargs -0 cat -- >> "./${1}/combined.bin"

echo "Running unpacker" >> ./${1}/${1}_log
./unpacker "./${1}/combined.bin" "./${1}/unpacked/output.bin" 0 >> ./${1}/${1}_log 2>&1

${2} -nodisplay -nodesktop -r "addpath(genpath('${3}')); init('$(pwd)/${1}/unpacked/output.bin.GPS_L1'); exit();" >> ./${1}/${1}_log 2>&1
