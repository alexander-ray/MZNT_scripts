#/bin/bash
# $1 is base name of bin files
# Bin files must be at same level or lower in directory structure
# $2 is path to matlab executable
# $3 is path to SDR code directory

# Directory should be created by inotify script
# Currently in correct subdirectory
mkdir ./unpacked
touch ./${1}_log

echo "Combining IF files" >> ./${1}_log
find . -type f -name "*.bin*" -print0 | sort -z | xargs -0 cat -- >> "./combined.bin"

echo "Running unpacker" >> ./${1}_log
./unpacker "./combined.bin" "./unpacked/output.bin" 0 >> ./${1}_log 2>&1

matlab -nodisplay -nodesktop -r "addpath(genpath('${3}')); init('$(pwd)/unpacked/output.bin.GPS_L1'); exit();" >> ./${1}_log 2>&1
