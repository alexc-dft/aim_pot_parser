# aim_pot_parser - An AIMPRO potential to .cube format parser
Scripts for setting up a regular grid of points for AIMPRO potential calculations and parsing the results to the .cube file format 
(potential values in Rydberg by default).

Please credit the code author(s) (Alex Christison, fixes by James Ramsey) in works arising from the use of this software.

Copyright (c) A Christison 2025 All Rights Reserved.  

**N.B. recurse submodules must be enabled to properly clone this repo: git clone --recurse-submodules repo_address**  

All routines & classes must have Google style docstrings: https://google.github.io/styleguide/pyguide.html

All python code should be run through Pylint: https://pylint.readthedocs.io/en/stable/

**NOTE:** these tools read/write entire files into memory to avoid poor performance due to I/O buffer thrashing. They will be memory intensive for particularly large files (i.e. those with ~ millions of lines).

### Requirements
To install all python package requirements in your python virtual environment do:  
pip install -r requirements.txt

Python version: python 3.11  
Requirements: see requirements.txt

Scripts can be made executable all locations in file system via chmod u+x and adding to PATH.

## Top level workflow

1. Generate a pot_file using potfile_gen
2. Run a potential job in the AIMPRO code
3. Use aimpot2cube to pass AIMPRO results into the .cube format

## potfile_gen usage
regGridPlot [options] [grid_vectors_input_file]

This script plots a regular grid in the required format for the potential job in the AIMPRO code that is valid for cubefile plotting.

### AIMPRO potential job documentation
https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html

### CUBE file format
https://www.quantum-espresso.org/Doc/INPUT_PP.html (&PLOT namelist, iflag = 3, output_format = 6)
https://paulbourke.net/dataformats/cube/

The output pot_file is written to the current working directory  

### Arguments
[options]  
-h, --help: display help dialogue  
-v, --verbose: turn on verbose output mode, this prints useful status info to screen  
-d, --debug: turn on debug mode (for developers only)  

[grid_vectors_input_file]  
Specifies the vectors & the number of their repeats defining the grid of points centered on each voxel of the parallelepiped plotting volume, as well as the origin of the parallelepiped plotting volume.  
The file is delimited by whitespace and has the format:  

Origin_x(float)  Origin_y(float)  Origin_z(float)  
Repeats_A(int)  A_x(float)  A_y(float)  A_z(float)  
Repeats_B(int)  B_x(float)  B_y(float)  B_z(float)  
Repeats_C(int)  C_x(float)  C_y(float)  C_z(float)  


All vectors are in atomic units (i.e. Bohr).  
Origin must be specified even if all values are zero.  

Repeats values must be >= 1.  
Vector components an have any valid float value.  
Origin components can have any valid float value.  

Floats are in 12.6 format.  

### Defining the potfile_gen input

It is often helpful to define grid with a reasonably dense sampling density within your system lattice.  
This ensures that the potential is being sampled with high enough resolution and avoids spurious data points from sampling periodic images.  

Unless a custom grid is required for a specific purpose, the FFT sampling grid density AIMPRO uses for a DFT calculation of your system is generally a suitable choice.  

For the case of example_input.in, it is designed around a 1x1x1 simple cubic diamond system with a single lattice constant of 6.74 Bohr and a sampling density of 36 data points in all dimensions of the unit cell, taken from the FFT grid density.  
The grid vectors are aligned with the lattice vectors.  

The calculation of grid vectors is as given:  

(1.0 0.0 0.0) x 6.74/36 = (0.187222 0.000000 0.000000)  
(0.0 1.0 0.0) x 6.74/36 = (0.000000 0.187222 0.000000)  
(0.0 0.0 0.0) x 6.74/36 = (0.000000 0.000000 0.187222)  

Sampling density therefore becomes the number of repeats, and by fixing the origin at (0.0 0.0 0.0) we obtain the contents of example_potfile_gen_input/example_input.in:  

0.000000 0.000000 0.000000  
36 0.187222 0.000000 0.000000  
36 0.000000 0.187222 0.000000  
36 0.000000 0.000000 0.187222  

The general form of this calculation is given as:  
(Lattice_vector_A) x Lattice_param_A / Sampling_density_in_A = (Grid_vector_A)  
(Lattice_vector_B) x Lattice_param_B / Sampling_density_in_B = (Grid_vector_B)  
(Lattice_vector_C) x Lattice_param_C / Sampling_density_in_C = (Grid_vector_C)  

Where:  

Sampling_density_in_A = Repeats_A  
Sampling_density_in_B = Repeats_B  
Sampling_density_in_C = Repeats_C  

And Origin == System origin i.e. generally (0.0 0.0 0.0)  

### Known issues
None  

## AIMPRO dat file & job docs

Potential job documentation: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html

## aimpot2cube usage
aimpot2cube [options] AIMPRO_output grid_vectors_input_file

This script parses the output from an AIMPRO potential job, specifically the sum of the external/local potental and Hartree potential
(using a pot_file generated by potfile_gen) into the cubefile (.cube) format (potential values in Rydberg by default).  

The backend of this script converts AIMRPO atomic positions to the atomic reference frame, using Jon Goss's gres script.  

By default the potential values are given in Rydberg, to match the default units that quantum espresso uses, other units can be specified  

### Perl script  
gres: https://www.staff.ncl.ac.uk/j.p.goss/MMG/Scripts/Output.html  
(Copyright (c) J.P. Goss 2024 All Rights Reserved.)

### CUBE file format
https://www.quantum-espresso.org/Doc/INPUT_PP.html (&INPUTPP namelist plot_num = 11; &PLOT namelist, iflag = 3, output_format = 6)
https://paulbourke.net/dataformats/cube/

### Arguments
[options]  
-h, --help: display help dialogue  
-v, --verbose: turn on verbose output mode, this prints useful status info to screen  
-d, --debug: turn on debug mode (for developers only)  
-pav, --print-average-v: prints a volume averaged (V_unit/bohr^3) value for the electrostaic potential, useful for convergence testing  
                        sampling grid densities (of grid with constant volume) for the potfile_gen input file  
-Ha, --Hartree: output potential in Hartee (default is Rydberg if none provided)  
-eV, --electron-volts: output potential in electron volts (default is Rydberg if none provided)  
-Ry, --Rydberg: output potential in Rydberg (default is Rydberg if none provided)  

AIMPRO_output  
The AIMRPO standard output file from a potential job, this can be a filepath  

grid_vectors_input_file  
the potfile_gen input file that was used for the AIMRPO potential job, this can be a filepath.  
See potfile_gen documentation.

**NOTE: this input file must be identical to the one used by potfile_gen to generate the input for the AIMPRO potential job**

### Known issues
None  
