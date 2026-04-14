# aim_pot_parser v1.4 - An AIMPRO potential job to .cube format parser
Scripts for setting up a regular grid of points for AIMPRO potential calculations and parsing the results to the .cube file format 
(potential values in Rydberg by default).

Please credit the code author(s) (Alex Christison, fixes by James Ramsey) in all works arising from the use of this software.

Copyright (c) A Christison 2026 All Rights Reserved.  

**NOTE:** these tools read/write entire files into memory to avoid poor performance due to I/O buffer thrashing. They will be memory intensive for particularly large files (i.e. those with ~ millions of lines).

## Developer & git specific info (Regular users ignore this section)

**N.B. recurse submodules must be enabled to properly clone this repo: git clone --recurse-submodules repo_address**  

All routines & classes must have Google style docstrings: https://google.github.io/styleguide/pyguide.html

All python code should be run through Pylint: https://pylint.readthedocs.io/en/stable/

The `aimpot2cube` and `potfile_gen` scripts can be made executable in all locations in file system via `chmod u+x` and adding to PATH.

## Version info
Version: 1.4
Version date: 14/04/26

## Requirements
Python version: python 3.11  
Requirements: see requirements.txt

A python virtual environment is generally required to install python packages on modern Debian based Linux distributions.

```
python3 -m venv ~/python_env
source ~/python_env/bin/activate
```

and to deactivate:

```
deactivate
```

For more info see: https://docs.python.org/3/library/venv.html

The `source ~/python_env/bin/activate` command can be added to the end of your `~/.bashrc` or `~/.bash_profile` to load your python virtual environment on startup if so desired.  

To install all python package requirements in your python virtual environment do
`pip install -r requirements.txt` in the root of the repository.

This code has only been tested for Debian 12 and Ubuntu 24.04 LTS Linux distributions, your mileage with other OSs and Linux distributions may vary. 

## Top level workflow

1. Generate a pot_file using potfile_gen
2. Run a potential job in the AIMPRO code
3. Use aimpot2cube to pass AIMPRO results into the .cube format

## potfile_gen usage
`potfile_gen [options] grid_vectors_input_file`

This script plots a regular grid in the required format for the potential job in the AIMPRO code that is valid for cubefile plotting.

### AIMPRO potential job documentation
https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html

### CUBE file format
https://www.quantum-espresso.org/Doc/INPUT_PP.html (&PLOT namelist, iflag = 3, output_format = 6)   
https://paulbourke.net/dataformats/cube/   

The output pot_file is written to the current working directory  

### Arguments
#### [options]  
`-h, --help`: display help dialogue  
`-v, --verbose`: turn on verbose output mode, this prints useful status info to screen  
`-q, --quiet` : silence all all non-error messages  
`-d, --debug`: turn on debug mode (for developers only)  
`-aif, --advanced-input-file`: use the advanced grid vectors input file format (origin, repeats & grid vectors) rather than the current one
                        (number of points along vector & (supercell) real space lattice vectors) (see end of README for details)  

#### grid_vectors_input_file  
Specifies the vectors & the number of their repeats defining the grid of sampling points placed on the corner of each voxel of the parallelepiped plotting volume, as well as the origin of the parallelepiped plotting volume, this can also be a filepath and/or compressed .bz2 archive to/of the file.  

The file is delimited by whitespace and has the format:  

Number_of_points_along_A(int)  A_x(float)  A_y(float)  A_z(float)  
Number_of_points_along_B(int)  B_x(float)  B_y(float)  B_z(float)  
Number_of_points_along_C(int)  C_x(float)  C_y(float)  C_z(float)  

Where A, B & C are real space lattice vectors.  

All vectors are in atomic units (i.e. Bohr).  
These grids always originate at (0.0, 0.0, 0.0).  

Number of points along a specified vector must be integers >= 1.  
Vector components can have any valid float value.  

Floats are in 12.6 format.  

### Defining the potfile_gen input

Much like MP k-point sampling, a suitably dense grid must be used for sampling the potential to ensure suitable convergence.  

The `-pci` or `--print-convergence-info` flag for the `aimpot2cube` parser enables the printing of the volume averaged potential and maximum variation of the potential to screen, these values can be used to convergence test the potential sampling grid densities.  

The AIMPRO FFT grid density is the absolute maximum workable grid density, by the nature of how FFT grids are used in DFT calculations densities higher than this yield no improvement to the sampling accuracy.  

The AIMPRO FFT grid density is often significantly more dense than required for applications that use cubefile potential data, these higher densities have significantly higher file storage (in the GB range) and AIMPRO runtime costs for no gain in scientific accuracy.  

In testing AIMPRO potential jobs using the FFT grid density as the potential sampling density in the `pot_file` took 50x longer to run with files 60x larger than the correctly converged potential sampling density for **no** improvement in scientific accuracy. As such it is **strongly** advised users avoid the use of over-converged grid densities.  

For computational expediency, it is recommended to converge the potential sampling grid density on a (pristine) unit cell of your system. Once converged, the number of sampling points along each of your lattice vectors can then be up-scaled in kind with the up-scaled lattice vectors when a supercell is produced from that unit cell.  

Throughout this process an equal number of points/bohr along each vector must be maintained.  

For example for lattice vectors with a a ratio of A:B:2C, there must be twice as many points along C as A & B for any & all sampling densities. In this case 1:1:2 is the sparsest grid that can be can used. This ratio can be checked against the FFT grid density as it will have the correct ratio of points along each vector. In this example the converged potential sampling grid density will be somewhere between 1:1:2 and the FFT grid density, generally on the sparser end so it is advised convergence testing is carried out starting from sparser and working up towards denser grids.

Once the converged potential sampling grid density for the (pristine) unit cell has been found, the number of points along each lattice vector must be scaled up in accordance with the supercell size. If for the previous example (of lattice vectors in the ratio A:B:2C), lattice vectors A & B increase by 4x the number of potential sampling points along A & B must also increase by 4x to keep the number of potential sampling points/bohr consistent along each lattice vector. Here no scaling will be applied to the number of potential sampling points along C, as C didn't change when producing the supercell.

For the case of example_input.in, it is designed around a 1x1x1 simple cubic diamond system with a lattice constant of 6.74 Bohr and a converged sampling density with 10 potential sampling points along all vectors of the cell.  

The (supercell) real space lattice vectors for a given cell geometry can be found by searching a corresponding AIMPRO output/ PAIM output for: ` unit vectors : real space`

e.g.:  

```
 unit vectors : real space, reciprocal space
     6.74000     0.00000     0.00000          0.93222     0.00000     0.00000
     0.00000     6.74000     0.00000          0.00000     0.93222     0.00000
     0.00000     0.00000     6.74000          0.00000     0.00000     0.93222
```

Combining the real space lattice vectors and sampling density gives an input file of the form:

```
10 6.74 0.00 0.00  
10 0.00 6.74 0.00  
10 0.00 0.00 6.74  
```

### Known issues
None  

## AIMPRO dat file & job docs

Potential job documentation: https://www.staff.ncl.ac.uk/j.p.goss/AIMPRO/restricted/docs/analysis/potential.html

## aimpot2cube usage
`aimpot2cube [options] AIMPRO_output grid_vectors_input_file`

This script parses the output from an AIMPRO potential job, specifically the sum of the external/local potential and Hartree potential
(using a pot_file generated by potfile_gen) into the cubefile (.cube) format (potential values in Rydberg by default).  

The backend of this script converts AIMRPO atomic positions to the atomic reference frame, using Jon Goss's gres script.  

By default the potential values are given in Rydberg, to match the default units that quantum espresso uses, other units can be specified.  

### Perl script  
gres: https://www.staff.ncl.ac.uk/j.p.goss/MMG/Scripts/Output.html  
(Copyright (c) J.P. Goss 2024 All Rights Reserved.)

### CUBE file format
https://www.quantum-espresso.org/Doc/INPUT_PP.html  
(&INPUTPP namelist plot_num = 11; &PLOT namelist, iflag = 3, output_format = 6)  
https://paulbourke.net/dataformats/cube/  

### Arguments
#### [options]  
`-h, --help`: display help dialogue  
`-v, --verbose`: turn on verbose output mode, this prints useful status info to screen  
`-q, --quiet` : silence all all non-error messages  
`-d, --debug`: turn on debug mode (for developers only)  
`-pci, --print-convergence-info:` prints a volume averaged (V_unit/bohr^3) value and maximum variation of the electrostatic potential, 
                            useful for convergence testing sampling grid densities (of grid with constant volume) for the potfile_gen input file  
`-aif, --advanced-input-file`: use the advanced grid vectors input file format (origin, repeats & grid vectors) rather than the current one
                        (number of points along vector & (supercell) real space lattice vectors) (see end of README for details)  
`-Ha, --Hartree`: output potential in Hartrees (default is Rydbergs if none provided)  
`-eV, --electron-volt`: output potential in electron volts (default is Rydbergs if none provided)  
`-Ry, --Rydberg`: output potential in Rydbergs (default is Rydbergs if none provided)  

#### AIMPRO_output  
The AIMRPO standard output file from a potential job, this can also be a filepath and/or compressed .bz2 archive to/of the file.  

#### grid_vectors_input_file  
the potfile_gen input file that was used for the AIMRPO potential job, this can also be a filepath and/or compressed .bz2 archive to/of the file.  
See potfile_gen documentation.

**NOTE: this input file must be identical to the one used by potfile_gen to generate the input for the AIMPRO potential job**

### Known issues
None  

# Advanced input file info

#### Advanced grid_vectors_input_file file format

This is the advanced input file format, the `-aif` or `--advanced-input-file` flag must be used for both scripts in order to read this file format.

Specifies the vectors & the number of their repeats defining the grid of sampling points placed on the corner of each voxel of the parallelepiped plotting volume, as well as the origin of the parallelepiped plotting volume, this can also be a filepath and/or compressed .bz2 archive to/of the file.  

The file is delimited by whitespace and has the format:  

Origin_x(float)  Origin_y(float)  Origin_z(float)  
Repeats_A(int)  A_x(float)  A_y(float)  A_z(float)  
Repeats_B(int)  B_x(float)  B_y(float)  B_z(float)  
Repeats_C(int)  C_x(float)  C_y(float)  C_z(float)  

Where A, B & C are real space lattice vectors.  

All vectors are in atomic units (i.e. Bohr).  
Origin must be specified even if all values are zero.  

Repeats values must be integers >= 1.  
Vector components an have any valid float value.  
Origin components can have any valid float value.  

Floats are in 12.6 format.  

### Defining the advanced potfile_gen input

It is often helpful to define grid with a reasonably dense potential sampling density within your system lattice.  
This ensures that the potential is being sampled with high enough resolution and avoids spurious data points from sampling periodic images.  

For the case of example_advanced_input.in, it is designed around a 1x1x1 simple cubic diamond system with a single lattice constant of 6.74 Bohr and a converged sampling density with 10 potential sampling points along all vectors of the cell.  
The grid vectors are aligned with the lattice vectors.  

The calculation of grid vectors is as given:  

(1.0 0.0 0.0) x 6.74/10 = (0.674 0.000 0.000)  
(0.0 1.0 0.0) x 6.74/10 = (0.000 0.674 0.000)  
(0.0 0.0 1.0) x 6.74/10 = (0.000 0.000 0.674)  

Sampling density therefore becomes the number of repeats, and by fixing the origin at (0.0 0.0 0.0) we obtain the contents of example_potfile_gen_input/example_advanced_input.in:  

```
0.0 0.0 0.0  
10 0.674 0.000 0.000
10 0.000 0.674 0.000
10 0.000 0.000 0.674
```

The general form of this calculation is given as:  

(Lattice_vector_A) x Lattice_param_A / Number_of_points_along_A = (Grid_vector_A)  
(Lattice_vector_B) x Lattice_param_B / Number_of_points_along_B = (Grid_vector_B)  
(Lattice_vector_C) x Lattice_param_C / Number_of_points_along_C = (Grid_vector_C)  

Where:  

Sampling_density_in_A = Repeats_A  
Sampling_density_in_B = Repeats_B  
Sampling_density_in_C = Repeats_C  

And Origin == System origin i.e. generally (0.0 0.0 0.0)  
