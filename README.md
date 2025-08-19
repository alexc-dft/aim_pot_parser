# aim_pot_parser - An AIMPRO potential to .cube format parser
Scripts for setting up a regular grid of points for AIMPRO potential calculations and parsing the results to the .cube file format

Please acknowledge the code author(s) (Alex Christison) in works arising from the use of this software.

Copyright (c) A Christison 2025 All Rights Reserved.

N.B. recurse submodules must be enabled to properly clone this repo: git clone --recurse-submodules <repo_address>

All routines & classes must have Google style docstrings: https://google.github.io/styleguide/pyguide.html

To install all python package requirements in your python virtual environment do: pip install -r requirements.txt

Python version: python 3.11
Requirements: see requirements.txt

Scripts can be made executable all locations in file system via chmod u+x and adding to PATH.

The output pot_file is written to the current working directory

# Overall usage workflow

1. Generate a pot_file using regGridPlot
2. Run a potential job in the AIMPRO code (atomic positons MUST be defined in au)
3. Use aimpot2cube to pass AIMPRO results into .cube format

# regGridPlot usage

regGridPlot [options] [grid_vectors_input_file]

[options]
-v, --verbose: Enables verbose output.

[grid_vectors_input_file]
Specifies the vectors & their repeats defining the grid.
The file is delimited by whitespace and has the format:

If no input file is specified the default input file from io_params will be used. This file is user editable (advanced: see ./low_level_scripts/python/io_params.py).

Repeats_A(int) A_x(float) A_y(float) A_z(float)
Repeats_B(int) B_x(float) B_y(float) B_z(float)
Repeats_C(int) C_x(float) C_y(float) C_z(float)

Repeats values must be >= 1.
Vector compoment values must be >= 0.0.

Integers are a maximum of 5 wide and floats are in 12.6 format.

# AIMPRO job docs

AIMPRO task documentation 
- Potential job: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html

The atomic positions in the potential job MUST be defined in au i.e. begin[atomic]{positions} MUST be specified.

Non au refs can be tranfomed to au as follows:

$ cp dat dat_old
$ gres -e dat
$ gres -x2o xyz.dat.all
$ InsertOTB otb.xyz.all dat_old > dat
(Optional) $ rm dat_old
Finally set REF to atomic in begin[REF]{positions} in dat file using your favourite text editor.

# aimpot2cube usage

aimpot2cube [options] AIMPRO_output [grid_vectors_input_file]

[options]
-v, --verbose: Enables verbose output.

AIMPRO_output
The standard AIMPRO output file

[grid_vectors_input_file]
See above.
NOTE: this file be the same as the one used by regGridPlot

TODO add further detail

Other documentation:
- CUBE format: https://paulbourke.net/dataformats/cube/
