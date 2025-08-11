#!/usr/bin/env python3
'''Regular Grid Plotter: regGridPlot [options] <input_filename.in>

This script plots a regular grid in the required format for the potential job in the AIMPRO code.

AIMPRO potential job documentation: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html

If no input file is specified the default input file in ./plot_input/default.in will be used. This file is user editable.

[options]
-d, --debug: Enables debug mode for verbose output.

<gridplot_input_file.in>
Specifies the vectors & their repeats defining the grid.
The file is delimited by whitespace and has the format:

Repeats_A(int) A_x(float) A_y(float) A_z(float)
Repeats_B(int) B_x(float) B_y(float) B_z(float)
Repeats_C(int) C_x(float) C_y(float) C_z(float)

Integers are a maximum of 5 wide and floats are in 12.6 format.
'''
import os
import sys
import argparse

# Filename constants
DEFAULT_INPUT_FILENAME = './plot_input/default.in'
OUTPUT_FILENAME = 'pot_file'

def main() -> None:
    filename = read_commmand_line()
    data = read_input_file(filename)
    write_pot_file(data)

def read_commmand_line() -> str:
    '''Gets input filename.

    If no input file is provided in command line the default input file is used.

    Args:
        None

    Returns:
        input_filename: Filename of input file

    Raises:
        Sets global debug flag if specified in cmd line args.
        Errors & exits with message if incorrect number of args detected.
    '''
    global debug

    return input_filename


def read_input_file(input_filename: str) -> tuple:
    '''Reads input file.

    Args:
        input_filename: Input filename/path.

    Returns:
        input_data: 2D tuple of grid vectors & number of repeats.

    Raises:
        Errors & exits with message if imput file opening &/ reading fails.
        Errors & exits with message if incorrect input file format detected.
    '''

    return input_data

def write_pot_file(input_data: tuple) -> None:
    '''Generates and writes out AIMPRO pot_file.

    Args:
        input_data: 2D tuple of grid vectors & number of repeats.

    Returns:
        None

    Raises:
        Errors & exits with message if output file opening &/ writing fails.
    '''

if __name__ == '__main__':
    main()
