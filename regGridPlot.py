#!/usr/bin/env python3
"""Regular Grid Plotter: regGridPlot [options] [input_file]

This script plots a regular grid in the required format for the potential job in the AIMPRO code.

AIMPRO potential job documentation: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html

If no input file is specified the default input file in ./plot_input/default.in will be used. This file is user editable.

[options]
-d, --debug: Enables debug mode for verbose output.

[input_file]
Specifies the vectors & their repeats defining the grid.
The file is delimited by whitespace and has the format:

Repeats_A(int) A_x(float) A_y(float) A_z(float)
Repeats_B(int) B_x(float) B_y(float) B_z(float)
Repeats_C(int) C_x(float) C_y(float) C_z(float)

Integers are a maximum of 5 wide and floats are in 12.6 format.
"""

import argparse
import sys

# Filename constants
DEFAULT_INPUT_FILENAME = "./plot_input/default.in"
OUTPUT_FILENAME = "pot_file"

def main() -> None:
    filename = read_commmand_line()
    data = read_input_file(filename)
    write_pot_file(data)

def read_commmand_line() -> str:
    """Gets input filename.

    If no input file is provided in command line the default input file is used.

    Args:
        None

    Returns:
        input_filename: Filename of input file

    Raises:
        Sets global verbose output flag if specified in cmd line args.
        Errors & exits with message if incorrect number of args detected.
    """
    global verbose_output

    parser = argparse.ArgumentParser(
                    prog="regGridPlot",
                    usage="regGridPlot [options] [input_file]",
                    description="Plot a regular grid for the AIMPRO potential job.",
                    epilog="AIMPRO potential job documentation: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output mode")
    parser.add_argument("input_file",nargs="?",help="input file, if none specified default input file is used.")

    args = parser.parse_args()
    verbose_output = args.verbose

    # Set to default input file i
    if args.input_file is None:
        input_filename = DEFAULT_INPUT_FILENAME
    else:
        input_filename = args.input_file[0]

    if args.verbose:
        print("Verbose output turned on\n")
        print(f"Input file: {input_filename}\n")

    return input_filename

def read_input_file(input_filename: str) -> tuple:
    """Reads input file.

    Args:
        input_filename: Input filename/path.

    Returns:
        input_data: 2D tuple of grid vectors & number of repeats.

    Raises:
        Errors & exits with message if imput file opening &/ reading fails.
        Errors & exits with message if incorrect input file format detected.
    """

    # Read in input file
    with open(input_filename,"r") as input_vectors:
        raw_vectors = input_vectors.read().splitlines()

    if len(raw_vectors) > 3:
        sys.exit("Error, incorrect format: ")

    print(raw_vectors)

    return input_data

def write_pot_file(input_data: tuple) -> None:
    """Generates and writes out AIMPRO pot_file.

    Args:
        input_data: 2D tuple of grid vectors & number of repeats.

    Returns:
        None

    Raises:
        Errors & exits with message if output file opening &/ writing fails.
    """

if __name__ == "__main__":
    main()
