# aimpot2cube
Scripts for setting up a regular grid for AIMPRO potential calculations and parsing the results to the .cube file format

N.B. recurse submodules must be enabled to properly clone this repo: git clone --recurse-submodules <repo_address>

AIMPRO task documentation 
- Potential job: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html
- Mulliken job: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/mull.html
- Analysis k-points: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/k-points.html

Other documentation:
- CUBE format: https://paulbourke.net/dataformats/cube/

All routines & classes must have Google style docstrings: https://google.github.io/styleguide/pyguide.html

They should be included in other repos as a git submodule via a symlink: https://stackoverflow.com/a/27770463

To install all python package requirements in your python virtual environment do: pip install -r requirements.txt

Python version: python 3.11
Requirements: see requirements.txt

Scripts can be made executable all locations in file system via chmod u+x and adding to PATH.

The output pot_file is written to the current working directory

# regGridPlot usage

regGridPlot [options] [grid_vectors_input_file]

[options]
-d, --debug: Enables debug mode for verbose output.

[grid_vectors_input_file] specifies the vectors & their repeats defining the grid.
The file is delimited by whitespace and has the format:

If no input file is specified the default input file  from io_params will be used. This file is user editable (advanced).

Repeats_A(int) A_x(float) A_y(float) A_z(float)
Repeats_B(int) B_x(float) B_y(float) B_z(float)
Repeats_C(int) C_x(float) C_y(float) C_z(float)

Integers are a maximum of 5 wide and floats are in 12.6 format.
