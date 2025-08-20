# aim_pot_parser - An AIMPRO potential to .cube format parser
Scripts for setting up a regular grid of points for AIMPRO potential calculations and parsing the results to the .cube file format

Please acknowledge the code author(s) (Alex Christison) in works arising from the use of this software.

Copyright (c) A Christison 2025 All Rights Reserved.  

N.B. recurse submodules must be enabled to properly clone this repo: git clone --recurse-submodules repo_address  

All routines & classes must have Google style docstrings: https://google.github.io/styleguide/pyguide.html

To install all python package requirements in your python virtual environment do:  
pip install -r requirements.txt

Python version: python 3.11  
Requirements: see requirements.txt

Scripts can be made executable all locations in file system via chmod u+x and adding to PATH.

The output pot_file is written to the current working directory

# Overall usage workflow

1. Generate a pot_file using potfileGen
2. Use any2any --atomic to convert atom postions in dat file to the atomic units reference frame
3. Run a potential job in the AIMPRO code (atomic positons MUST be defined in au)
4. Use aimpot2cube to pass AIMPRO results into .cube format

# potfileGen usage
regGridPlot [options] [grid_vectors_input_file]

This script plots a regular grid in the required format for the potential job in the AIMPRO code.

AIMPRO potential job documentation: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html

The output pot_file is written to the current working directory

[options]  
-h, --help: display help dialogue  
-v, --verbose: Enables verbose output  

[grid_vectors_input_file]  
Specifies the vectors & their repeats defining the grid.  
The file is delimited by whitespace and has the format:

If no grid vectors input file is specified the default input file from common_io will be used. This file is user editable (advanced: see ./low_level_scripts/python/common_io.py).

Repeats_A(int) A_x(float) A_y(float) A_z(float)  
Repeats_B(int) B_x(float) B_y(float) B_z(float)  
Repeats_C(int) C_x(float) C_y(float) C_z(float)

Repeats values must be >= 1.  
Vector compoment values must be >= 0.0.

Floats are in 12.6 format.

Known issues:  
None  

# any2any usage  
any2any [options] (--atomic | --intp | --intc | --angstroms | --scale SCALE) dat_file  

This script converts AIMRPO atomic positions using any reference frame to any other reference frame based on user selection, using Jon Goss's gres, InsertOTB & otb2intp Perl scripts.  

Atom positions documentation: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/positions.html  

Perl scripts
gres: https://www.staff.ncl.ac.uk/j.p.goss/MMG/Scripts/Output.html  
InsertOTB: https://www.staff.ncl.ac.uk/j.p.goss/MMG/Scripts/OTB+XYZ.html  
otb2intp: https://www.staff.ncl.ac.uk/j.p.goss/MMG/Scripts/DataFiles.html  
(Copyright (c) J.P. Goss 2024, 2015, 2011 All Rights Reserved.)  

[options]  
-h, --help: display help dialogue  
-rb, --retain_bak: Retains backup copy of datafile (dat_file.bak)  

(--atomic | --intp | --intc | --angstroms | --scale SCALE)  
-au, --atomic: convert to atomic reference frame  
-p, --intp: convert to int-p reference frame  
-c, --intc: convert to int-c reference frame  
-ang, --angstroms: convert to angstroms reference frame  
-s SCALE, --scale SCALE  
                convert to atomic reference frame, scaled by provided float value SCALE  

The above options are mutually exclusive and required.  

dat_file  
AIMPRO dat file, this must follow the dat.xxx file name convention  

Known issues:  
The script is unable to account for depreciated definitions of the lattice parameters (e.g. a0=...) due to limitations of otb2intp.  
As these are depreciated this is not expected to be a frequent issue, however, example files in the docs still use the a0 definition so care must be taken to change a0= to params= in lattice{} if using these.  

# AIMPRO dat file & job docs

The atomic positions in the potential job MUST be defined in au i.e. begin[atomic]{positions} MUST be specified.

any2any --atomic can be used to convert the atom positions in a dat file to the atomic reference frame from any other reference frame.

Atom positions documentation: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/positions.html  
Potential job documentation: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html

# aimpot2cube usage
aimpot2cube [options] AIMPRO_output [grid_vectors_input_file]

TODO Add further description here

CUBE file format documentation: https://paulbourke.net/dataformats/cube/

[options]  
-h, --help: display help dialogue  
-v, --verbose: Enables verbose output

AIMPRO_output  
The standard AIMPRO output file

[grid_vectors_input_file]  
See above.

NOTE: this file must be the same as the one used by potfileGen

Known issues:  
None  
