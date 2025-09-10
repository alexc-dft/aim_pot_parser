#!/usr/bin/env bash

# This script manages the test suite and checks the tests are sucessful

# set -xv

test_list=("potfile_gen/" "aimpot2cube/")

declare -a failed_test_array=()

#***potfile_gen test***

test_dir=${test_list[0]}

# Setup files
cd $test_dir

test=${test_dir%/}

# Run potfile_gen
python ../../potfile_gen test.in.benchmark || { echo "Error: potfile_gen failed to run"; exit 2; }

# Diff for result
diff_str=$(diff "pot_file.benchmark" "pot_file")

# Check diff
if [ "$diff_str" != "" ]; then
    failed_test_array+=($test_dir)
    echo "$diff_str" > ${test}.diff
fi

cd ../

#***aimpot2cube test***

test_dir=${test_list[1]}

# Setup files
cd $test_dir

test=${test_dir%/}

cp "AIM.sh.o.benchmark" "AIM.sh.o.test"

# Run potfile_gen
python ../../aimpot2cube AIM.sh.o.test test.in.benchmark || { echo "Error: aimpot2cube failed to run"; exit 3; }

# Diff for result
diff_str=$(diff "AIM.sh.o.test.cube.benchmark" "AIM.sh.o.test.cube")

# Check diff
if [ "$diff_str" != "" ]; then
    failed_test_array+=($test_dir)
    echo "$diff_str" > ${test}.diff
fi

cd ../


# Check if we passed all tests
if [ ${#failed_test_array[@]} -eq 0 ]; then
    { echo "Success: all tests passed"; exit 0; }
else
    { echo "Error: failed test(s) in: ${failed_test_array[@]}"; exit 1; }
fi
