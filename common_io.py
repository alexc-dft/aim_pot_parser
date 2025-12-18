# Copyright (c) A Christison 2025 All Rights Reserved.

"""common_io: Common & I/O

This module stores the shared routines and I/O parameters for the aim_pot_parser repo.

The I/O parameters can be user reconfigured - recommended only for advanced users.

Known issues:
None
"""

# System modules
from pathlib import Path
from typing import Optional
import bz2
import re
import sys

# Wrangle submodule path
# !!!Note __file__ isn't always safe, e.g. in non-local imported modules!!!
SUBMODULE_PATH = Path(__file__).resolve().parent  / "aim_utils"     #pylint: disable=wrong-import-position
SUBM_PATH_STR = SUBMODULE_PATH.absolute().as_posix()                #pylint: disable=wrong-import-position

# Add path to aim_utils directory root
sys.path.append(SUBM_PATH_STR)  #pylint: disable=wrong-import-position

# Third party modules
import numpy as np
from numba import jit
import const as c   #pylint: disable=import-error

# Module development info
VERSION_NUMBER = "1.0"                                              #pylint: disable=duplicate-code
VERSION_DATE = "16/12/2025"                                         #pylint: disable=duplicate-code
AUTHORS = "Alex Christison"                                         #pylint: disable=duplicate-code
COPYRIGHT = "Copyright (c) A Christison 2025 All Rights Reserved"   #pylint: disable=duplicate-code

# Filename constants

# Regular Grid Plotter output file
POT_OUTPUT_FILENAME = "pot_file"

# aimpot2cube passer output file
CUBE_OUTPUT_FILENAME = ".cube"

# AIMPRO parser shared I/O routines

def read_grid_vectors(grid_vectors_input_file: str, verbose_output: Optional[bool] = False) -> tuple[object, object, object]:
    """Reads grid vectors and repeats from input file using the current input file format (grid density and real space lattice vectors)

    The grid of points is regenerated to validate the points in the AIMPRO output.

    Args:
        grid_vectors_input_file: Grid vectors input filename/path
        verbose_output (Optional, default False): turns on verbose output mode

    Returns:
        repeats: number of repeats of each vector
        vectors: grid vectors
        origin: parallelepiped grid origin (hardcoded to (0.0 0.0 0.0) in this imput file format)

    Raises:
        Errors & exits with message if incorrect input file format detected.
        Errors & exits with message if incorrect input values are detected.
    """

    # Define lists to store real space lattice vectors & grid_density
    grid_density = np.zeros((3), dtype=int)
    lattice_vectors = np.zeros((3, 3))
    # Origin hard coded to (0.0, 0.0, 0.0) in this input file format
    origin = np.zeros((3))

    # Read in input file, handling bzip2 archives if detected
    if re.search(c.RE_BZIP_FILE, grid_vectors_input_file):
        with bz2.open(grid_vectors_input_file, "rt") as infile:
            raw_input = infile.readlines()
    else:
        with open(grid_vectors_input_file, "r", encoding="UTF-8") as infile:
            raw_input = infile.readlines()

    if len(raw_input) != 3:
        raise Exception(f"incorrect input file format - {grid_vectors_input_file} must have only 3 rows")

    index = 0
    for row in raw_input:

        # Split in individual items
        split_row = row.split()

        if len(split_row) != 4:
            raise Exception(f"incorrect input file format - {grid_vectors_input_file} origin row must have only 4 columns")

        # Cast grid_density to integer and add to numpy array
        split_row[0] = int(split_row[0])
        grid_density[index] = np.array(split_row[0])

        # Map vectors to floats and add to numpy array
        split_row[1:4] = map(float,split_row[1:4])
        lattice_vectors[index, :] = np.array(split_row[1:4])

        # Increment index
        index+=1

    # Error checking to ensure input values are valid
    if any(grid_density < 1):
        raise ValueError(f"grid density values in {grid_vectors_input_file} must be integers >= 1")

    # Calculate grid vectors from real space lattice vectors and grid density
    lattice_vectors /= grid_density[:, None]

    # Write out grid vectors input if verbose_output enabled
    if verbose_output:
        print("Input grid vector data:\n")
        print(f"{origin[0]:12.6f} {origin[1]:12.6f} {origin[2]:12.6f}")
        for i, value in enumerate(grid_density):
            print(f"{value:5d} {lattice_vectors[i, 0]:12.6f} {lattice_vectors[i, 1]:12.6f} {lattice_vectors[i, 2]:12.6f}")
        print("\n")

    return grid_density, lattice_vectors, origin


def read_grid_vectors_legacy_input(grid_vectors_input_file: str, verbose_output: Optional[bool] = False) -> tuple[object, object, object]:
    """Reads grid vectors and repeats from input file using the legacy input file format (origin, grid vectors and repeats)

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

    # Read in input file, handling bzip2 archives if detected
    if re.search(c.RE_BZIP_FILE, grid_vectors_input_file):
        with bz2.open(grid_vectors_input_file, "rt") as infile:
            raw_input = infile.readlines()
    else:
        with open(grid_vectors_input_file, "r", encoding="UTF-8") as infile:
            raw_input = infile.readlines()

    if len(raw_input) != 4:
        raise Exception(f"incorrect input file format - legacy {grid_vectors_input_file} must have only 4 rows")

    index = 0
    for row in raw_input:

        # Split in individual items
        split_row = row.split()

        if index == 0 and len(split_row) != 3:
            raise Exception(f"incorrect input file format - legacy {grid_vectors_input_file} origin row must have only 3 columns")
        if index > 0 and len(split_row) != 4:
            raise Exception(f"incorrect input file format - legacy {grid_vectors_input_file} grid vectors row must have only 4 columns")

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
        raise ValueError(f"repeats values in {grid_vectors_input_file} must be integers >= 1")

    # Write out grid vectors input if verbose_output enabled
    if verbose_output:
        print("Input grid vector data:\n")
        print(f"{origin[0]:12.6f} {origin[1]:12.6f} {origin[2]:12.6f}")
        for i, value in enumerate(repeats):
            print(f"{value:5d} {vectors[i, 0]:12.6f} {vectors[i, 1]:12.6f} {vectors[i, 2]:12.6f}")
        print("\n")

    return repeats, vectors, origin

@jit
def generate_grid_points(repeats: object, vectors: object, origin: object, verbose_output: Optional[bool] = False) -> object:#pylint:disable=too-many-arguments,too-many-positional-arguments
    """Generates the pot_file grid points and adds adds them to a numpy array.

    Args:
        repeats: number of repeats of each vector
        vectors: grid vectors
        origin: parallelepiped grid origin

    Returns:
        grid_points: numpy array of generated grid points

    Raises:
        None
    """

    if verbose_output:
        print("Generating grid points\n")

    # Get required array length
    num_grid_points = np.prod(repeats)
    grid_points = np.zeros((num_grid_points, 3))

    # Declare row counter
    row_count = 0

    for ia in range(0, repeats[0]):
        for ib in range(0, repeats[1]):
            for ic in range(0, repeats[2]):

                # Calculate grid point and add to array
                grid_points[row_count, :] = origin  + ia * vectors[0, :] \
                                                    + ib * vectors[1, :] \
                                                    + ic * vectors[2, :]

                # Handle sign flip issue when grid_point values ~~ 0.0, due to quirks of floats
                # Forces -0.0 to be 0.0
                if np.allclose(grid_points[row_count, :], np.zeros(3)):
                    grid_points[row_count, :] = np.zeros(3)

                # Increment row counter
                row_count+=1

    if verbose_output:
        print(f"Generated {num_grid_points} grid points\n")

    return grid_points, num_grid_points
