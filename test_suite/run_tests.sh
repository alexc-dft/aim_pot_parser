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

# Run potfile_gen
python ../../potfile_gen test.in.benchmark || { echo "Error: potfile_gen failed to run">&2; exit 2; }

# Diff for result
diff_str=$(diff "pot_file.benchmark" "pot_file"); [ $? -gt 1 ] && exit 4

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

# Standard

cp "AIM.sh.o.benchmark" "AIM.sh.o.test"

# Run aimpot2cube
python ../../aimpot2cube -eV AIM.sh.o.test test.in.benchmark || { echo "Error: aimpot2cube failed to run">&2; exit 3; }

# Diff for result
diff_str=$(diff "AIM.sh.o.test_eV.cube.benchmark" "AIM.sh.o.test_eV.cube"); [ $? -gt 1 ] && exit 4

# Check diff
if [ "$diff_str" != "" ]; then
    failed_test_array+=($test_dir)
    echo "$diff_str" > ${test}.diff
fi

# Hartree

cp "AIM.sh.o_hartree.benchmark" "AIM.sh.o_hartree.test"

# Run aimpot2cube
python ../../aimpot2cube -Ha AIM.sh.o_hartree.test test_hartree.in.benchmark || { echo "Error: aimpot2cube failed to run">&2; exit 3; }

# Diff for result
diff_str=$(diff "AIM.sh.o_hartree.test_Ha.cube.benchmark" "AIM.sh.o_hartree.test_Ha.cube"); [ $? -gt 1 ] && exit 4

test_hartree="${test}-hartree"

# Check diff
if [ "$diff_str" != "" ]; then
    failed_test_array+=($test_hartree)
    echo "$diff_str" > ${test_hartree}.diff
fi

# Rydberg

cp "AIM.sh.o_rydberg.benchmark" "AIM.sh.o_rydberg.test"

# Run aimpot2cube
python ../../aimpot2cube AIM.sh.o_rydberg.test test_rydberg.in.benchmark || { echo "Error: aimpot2cube failed to run">&2; exit 3; }

# Diff for result
diff_str=$(diff "AIM.sh.o_rydberg.test_Ry.cube.benchmark" "AIM.sh.o_rydberg.test_Ry.cube"); [ $? -gt 1 ] && exit 4

test_rydberg="${test}-rydberg"

# Check diff
if [ "$diff_str" != "" ]; then
    failed_test_array+=($test_rydberg)
    echo "$diff_str" > ${test_rydberg}.diff
fi

cd ../


# Check if we passed all tests
if [ ${#failed_test_array[@]} -eq 0 ]; then
    { echo "Success: all tests passed" >&2; exit 0; }
else
    { echo "Error: failed test(s) in: ${failed_test_array[@]}" >&2; exit 1; }
fi
