#!/usr/bin/env bash

# This script manages the test suite and checks the tests are sucessful

# set -xv

test_list=("potfile_gen/" "aimpot2cube/")

declare -a failed_test_array=()

#***potfile_gen cleanup***

test_dir=${test_list[0]}

# Setup files
cd $test_dir

test=${test_dir%/}

# Remove files if they exist

if [ -f pot_file_default ]; then
    rm "pot_file_default"
fi

test_default="${test}-default"

if [ -f ${test_default}.diff ]; then
    rm "${test_default}.diff"
fi

if [ -f pot_file ]; then
    rm "pot_file"
fi

if [ -f ${test}.diff ]; then
    rm "${test}.diff"
fi

cd ../

#***aimpot2cube cleanup***

test_dir=${test_list[1]}

# Setup files
cd $test_dir

test=${test_dir%/}

# Remove files if they exist

# Default

if [ -f AIM.sh.o_default.test ]; then
    rm "AIM.sh.o_default.test"
fi

if [ -f AIM.sh.o_default.test.cube ]; then
    rm "AIM.sh.o_default.test.cube"
fi

test_default="${test}-default"

if [ -f ${test_default}.diff ]; then
    rm "${test_default}.diff"
fi

# Standard

if [ -f AIM.sh.o.test ]; then
    rm "AIM.sh.o.test"
fi

if [ -f AIM.sh.o.test.cube ]; then
    rm "AIM.sh.o.test.cube"
fi

if [ -f ${test}.diff ]; then
    rm "${test}.diff"
fi

# Hartree

if [ -f AIM.sh.o_hartree.test ]; then
    rm "AIM.sh.o_hartree.test"
fi

if [ -f AIM.sh.o_hartree.test.cube ]; then
    rm "AIM.sh.o_hartree.test.cube"
fi

test_hartree="${test}-hartree"

if [ -f ${test_hartree}.diff ]; then
    rm "${test_hartree}.diff"
fi

cd ../

{ echo "Success: test suite cleanup finished"; exit 0; }
