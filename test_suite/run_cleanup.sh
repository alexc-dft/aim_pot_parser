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

test_advanced_input="${test}-advanced-input"

if [ -f pot_file_advanced_input ]; then
    rm "pot_file_advanced_input"
fi

if [ -f ${test_advanced_input}.diff ]; then
    rm "${test_advanced_input}.diff"
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

# Standard

if [ -f AIM.sh.o.test ]; then
    rm "AIM.sh.o.test"
fi

if [ -f AIM.sh.o.test_eV.cube ]; then
    rm "AIM.sh.o.test_eV.cube"
fi

if [ -f ${test}.diff ]; then
    rm "${test}.diff"
fi

# Hartree

if [ -f AIM.sh.o_hartree.test ]; then
    rm "AIM.sh.o_hartree.test"
fi

if [ -f AIM.sh.o_hartree.test_Ha.cube ]; then
    rm "AIM.sh.o_hartree.test_Ha.cube"
fi

test_hartree="${test}-hartree"

if [ -f ${test_hartree}.diff ]; then
    rm "${test_hartree}.diff"
fi

# Rydberg

if [ -f AIM.sh.o_rydberg.test ]; then
    rm "AIM.sh.o_rydberg.test"
fi

if [ -f AIM.sh.o_rydberg.test_Ry.cube ]; then
    rm "AIM.sh.o_rydberg.test_Ry.cube"
fi

test_rydberg="${test}-rydberg"

if [ -f ${test_rydberg}.diff ]; then
    rm "${test_rydberg}.diff"
fi

# Species order

if [ -f AIM.sh.o_species_order.test ]; then
    rm "AIM.sh.o_species_order.test"
fi

if [ -f AIM.sh.o_species_order.test_Ry.cube ]; then
    rm "AIM.sh.o_species_order.test_Ry.cube"
fi

test_species_order="${test}-species-order"

if [ -f ${test_species_order}.diff ]; then
    rm "${test_species_order}.diff"
fi

cd ../

{ echo "Success: test suite cleanup finished" >&2; exit 0; }
