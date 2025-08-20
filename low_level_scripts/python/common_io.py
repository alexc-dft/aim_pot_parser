# Copyright (c) A Christison 2025 All Rights Reserved.

"""common_io: Common & I/O

This module stores the shared routines and I/O parameters for the aim_pot_parser repo.

The I/O parameters  can be user reconfigured - recommended only for advanced users.

Known issues:
None
"""

from pathlib import Path
import numpy as np

# Module development info
VERSION_NUMBER = "0.1"
VERSION_DATE = "12/08/2025"
AUTHORS = "Alex Christison"
COPYRIGHT = "Copyright (c) A Christison 2025 All Rights Reserved"

# Filename constants

# Define filepath relative to script location
DEFAULT_POT_INPUT_FILENAME = Path(__file__).resolve().parents[2]  / "plot_input" / "default.in" # !!!Note __file__ isn't always safe, e.g. in non-local imported modules!!!

# Regular Grid Plotter output file
POT_OUTPUT_FILENAME = "pot_file"

# aimpot2cube passer output file
CUBE_OUTPUT_FILENAME = ".cube"

# AIMPRO parser shared I/O routines

def read_grid_vectors(grid_vectors_input_file: str) -> object:
    """Reads grid vectors an repeats from input file

    The grid of points is regenerated to validate the points in the AIMPRO output.


    Args:
        grid_vectors_input_file: Grid vectors input filename/path

    Returns:
        repeats: number of repeats of each vector
        vectors: grid vectors

    Raises:
        Errors & exits with message if incorrect input file format detected.
        Errors & exits with message if incorrect input values are detected.
    """

    # Define lists to store vectors & their repeats
    repeats = np.zeros([3], dtype=int)
    vectors = np.zeros([3, 3])

    # Read in input file
    with open(grid_vectors_input_file,"r") as infile:
        # Split into rows
        raw_input = infile.read().splitlines()

    if len(raw_input) != 3:
        raise Exception(f"incorrect input file format - {input_filename} must have only 3 rows")

    index = 0
    for row in raw_input:

        # Split in individual items
        split_row = row.split()

        if len(split_row) != 4:
            raise Exception(f"incorrect input file format - {input_filename} must have only 4 columns")

        # Cast repeats to integer and add to numpy array
        split_row[0] = int(split_row[0])
        repeats[index] = np.array(split_row[0])

        # Map vectors to floats and add to numpy array
        split_row[1:4] = map(float,split_row[1:4])
        vectors[index, :] = np.array(split_row[1:4])

        # Increment index
        index+=1

    # Error checking to ensure input values are valid
    if any(repeats < 1):
        raise ValueError(f"repeats values in {grid_vectors_input_file} must be >= 1")
    if np.any(vectors < 0.0):
        raise ValueError(f"grid vector values in {grid_vectors_input_file} must be > 0.0")

    return repeats, vectors
