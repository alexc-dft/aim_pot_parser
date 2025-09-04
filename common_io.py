# Copyright (c) A Christison 2025 All Rights Reserved.

"""common_io: Common & I/O

This module stores the shared routines and I/O parameters for the aim_pot_parser repo.

The I/O parameters  can be user reconfigured - recommended only for advanced users.

Known issues:
None
"""

# System modules
from pathlib import Path
from typing import Optional

# Third party modules
import numpy as np

# Module development info
VERSION_NUMBER = "0.2"
VERSION_DATE = "04/09/2025"
AUTHORS = "Alex Christison"
COPYRIGHT = "Copyright (c) A Christison 2025 All Rights Reserved"

# Filename constants

# Define filepath relative to script location
DEFAULT_POT_INPUT_FILENAME = Path(__file__).resolve().parents[0]  / "plot_input" / "default.in" # !!!Note __file__ isn't always safe, e.g. in nonlocal imported modules!!!

# Regular Grid Plotter output file
POT_OUTPUT_FILENAME = "pot_file"

# aimpot2cube passer output file
CUBE_OUTPUT_FILENAME = ".cube"

# AIMPRO parser shared I/O routines

def read_grid_vectors(grid_vectors_input_file: str, verbose_output: Optional[bool] = False) -> tuple[object, object, object]:
    """Reads grid vectors an repeats from input file

    The grid of points is regenerated to validate the points in the AIMPRO output.


    Args:
        grid_vectors_input_file: Grid vectors input filename/path
        verbose_output (Optional, default False): turns on verbose output mode

    Returns:
        repeats: number of repeats of each vector
        vectors: grid vectors
        origin: parallelepiped grid origin

    Raises:
        Errors & exits with message if incorrect input file format detected.
        Errors & exits with message if incorrect input values are detected.
    """

    # Define lists to store vectors & their repeats
    repeats = np.zeros((3), dtype=int)
    vectors = np.zeros((3, 3))
    origin = np.zeros((3))

    # Read in input file
    with open(grid_vectors_input_file,"r",encoding="UTF-8") as infile:
        # Split into rows
        raw_input = infile.readlines()

    if len(raw_input) != 4:
        raise Exception(f"incorrect input file format - {grid_vectors_input_file} must have only 4 rows")

    index = 0
    for row in raw_input:

        # Split in individual items
        split_row = row.split()

        if index == 0 and len(split_row) != 3:
            raise Exception(f"incorrect input file format - {grid_vectors_input_file} origin row must have only 3 columns")
        if index > 0 and len(split_row) != 4:
            raise Exception(f"incorrect input file format - {grid_vectors_input_file} grid vectors row must have only 4 columns")

        if index == 0:
            # Map origin components to float and add to numpy array
            split_row[0:3] = map(float,split_row[0:3])
            origin[:] = np.array(split_row[0:3])

        else:
            # Cast repeats to integer and add to numpy array
            split_row[0] = int(split_row[0])
            repeats[index-1] = np.array(split_row[0])

            # Map vectors to floats and add to numpy array
            split_row[1:4] = map(float,split_row[1:4])
            vectors[index-1, :] = np.array(split_row[1:4])

        # Increment index
        index+=1

    # Error checking to ensure input values are valid
    if any(repeats < 1):
        raise ValueError(f"repeats values in {grid_vectors_input_file} must be >= 1")

    # Write out grid vectors input if verbose_output enabled
    if verbose_output:
        print("Input grid vector data:\n")
        print(f"{origin[0]:12.6f} {origin[1]:12.6f} {origin[2]:12.6f}")
        for i, value in enumerate(repeats):
            print(f"{value:5d} {vectors[i, 0]:12.6f} {vectors[i, 1]:12.6f} {vectors[i, 2]:12.6f}")
        print("\n")

    return repeats, vectors, origin
