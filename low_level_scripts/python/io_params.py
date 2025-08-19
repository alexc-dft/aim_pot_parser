# Copyright (c) A Christison 2025 All Rights Reserved.

"""I/O parameters

This module stores the I/O parameters for the aim_pot_parser repo.

These can be user reconfigured - recommened only for advanced users.
"""

import os

# Module development info
VERSION_NUMBER = "0.1"
VERSION_DATE = "12/08/2025"
AUTHORS = "Alex Christison"
COPYRIGHT = "Copyright (c) A Christison 2025 All Rights Reserved"

# Filename constants

DEFAULT_POT_INPUT_FILENAME = os.path.dirname(__file__) +  "/plot_input/default.in" # Define filepath relative to script location

# Regular Grid Plotter output file
POT_OUTPUT_FILENAME = "/pot_file"

# aimpot2cube passer output file
CUBE_OUTPUT_FILENAME = "/pot_file.cube"
