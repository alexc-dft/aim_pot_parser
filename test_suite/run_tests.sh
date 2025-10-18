#!/usr/bin/env bash

# This script manages the test suite and checks the tests are sucessful

# set -xv

# Run initial cleanup
bash ./run_cleanup.sh

test_list=("potfile_gen/" "aimpot2cube/")

declare -a failed_test_array=()

#***potfile_gen test***

test_dir=${test_list[0]}


# Setup files
cd $test_dir

test=${test_dir%/}

# Run potfile_gen for default input
python ../../potfile_gen || { echo "Error: potfile_gen failed to run"; exit 2; }

mv "pot_file" "pot_file_default"

# Diff for result
diff_str=$(diff "pot_file_default.benchmark" "pot_file_default")

test_default="${test}-default"

# Check diff
if [ "$diff_str" != "" ]; then
    failed_test_array+=($test_default)
    echo "$diff_str" > ${test_default}.diff
fi

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

cp "AIM.sh.o_default.benchmark" "AIM.sh.o_default.test"

# Run aimpot2cube for default input
python ../../aimpot2cube AIM.sh.o_default.test || { echo "Error: aimpot2cube failed to run"; exit 3; }

# Diff for result
diff_str=$(diff "AIM.sh.o_default.test.cube.benchmark" "AIM.sh.o_default.test.cube")

test_default="${test}-default"

# Check diff
if [ "$diff_str" != "" ]; then
    failed_test_array+=($test_default)
    echo "$diff_str" > ${test_default}.diff
fi


cp "AIM.sh.o.benchmark" "AIM.sh.o.test"

# Run aimpot2cube
python ../../aimpot2cube AIM.sh.o.test test.in.benchmark || { echo "Error: aimpot2cube failed to run"; exit 3; }

# Diff for result
diff_str=$(diff "AIM.sh.o.test.cube.benchmark" "AIM.sh.o.test.cube")

# Check diff
if [ "$diff_str" != "" ]; then
    failed_test_array+=($test_dir)
    echo "$diff_str" > ${test}.diff
fi

cp "AIM.sh.o_hartree.benchmark" "AIM.sh.o_hartree.test"

# Run aimpot2cube
python ../../aimpot2cube -ha AIM.sh.o_hartree.test test_hartree.in.benchmark || { echo "Error: aimpot2cube failed to run"; exit 3; }

# Diff for result
diff_str=$(diff "AIM.sh.o_hartree.test.cube.benchmark" "AIM.sh.o_hartree.test.cube")

test_hartree="${test}-hartree"

# Check diff
if [ "$diff_str" != "" ]; then
    failed_test_array+=($test_hartree)
    echo "$diff_str" > ${test_hartree}.diff
fi

cd ../


# Check if we passed all tests
if [ ${#failed_test_array[@]} -eq 0 ]; then
    { echo "Success: all tests passed"; exit 0; }
else
    { echo "Error: failed test(s) in: ${failed_test_array[@]}"; exit 1; }
fi
