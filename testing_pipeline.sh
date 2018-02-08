#!/bin/bash
# $1 is base name of bin files
# Bin files must be at same level or lower in directory structure
# $2 is path to SDR code directory

#mkdir ${1}
mkdir ./${1}/unpacked
touch ./${1}/${1}_log

echo "Combining IF files" >> ./${1}/${1}_log
find . -type f -name "${1}.bin*" -print0 | sort -z | xargs -0 cat -- >> "./${1}/combined.bin"

echo "Running unpacker" >> ./${1}/${1}_log
./unpacker "./${1}/combined.bin" "./${1}/unpacked/output.bin" 0 >> ./${1}/${1}_log 2>&1

#matlab_cmd="addpath(genpath('${2}')); init('${pwd}/${1}/unpacked/output.bin.GPS_L1'); exit();"
#/Applications/MATLAB_R2016b.app/bin/matlab -nodisplay -nodesktop -r $matlab_cmd 
/Applications/MATLAB_R2016b.app/bin/matlab -nodisplay -nodesktop -r "addpath(genpath('${2}')); init('$(pwd)/${1}/unpacked/output.bin.GPS_L1'); exit();" >> ./${1}/${1}_log 2>&1
