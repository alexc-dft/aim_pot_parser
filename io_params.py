"""I/O parameters

This module stores the I/O parameters for the aim_pot_parser repo.

These can be user reconfigured - recommened only for advanced users.
"""

import os

# Filename constants

DEFAULT_POT_INPUT_FILENAME = os.path.dirname(__file__) +  "/plot_input/default.in" # Define filepath relative to script location

# Regular Grid Plotter output file
POT_OUTPUT_FILENAME = "/pot_file"

# aimpot2cube passer output file
CUBE_OUTPUT_FILENAME = "/pot_file.cube"
