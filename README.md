# inductive-coil-design-automation
The aim of this repository is to automate the design of simple inductive coils. 

# Features
There are several scripts which allow the user to create inductive coils of different shapes. The relevant scripts are detailed below:
### *new_coil.py*
create inductive coils of different shapes with
- variable turn number, including partial turns
- customizable outer diameter, track width, track gap, etc.
- a front Cu layer and a back Cu layer

### *coil_circle.py* and *coil_square.py*
create a simple square coil or a simple circular coil with the same customizable options as in *new_coil.py*.
The difference is that these scripts are only capable of creating a square coil and circular coil respectively. As another difference, the circular coil is made of curved arcs, whereas it is made out of tiny straight lines in *new_coil.py*.

These two scripts can be used simply by executing their main function and optionally adjusting the parameters in the main function directly in the code. 

# Usage of *new_coil.py*
*src/new_coil.py* is the main script, and this is the help message it prints when executed without any arguments:
```
Usage:

            python3 src/new_coil.py -option value

                    -vN export an N-gonal inductor instead of default helical inductor

                        i.e. -v3 for triangle, -v4 for square, -v6 for hexagon

                    -i long  inner diameter of coil in microns

                    -o long  outer diameter of coil in microns

                    -w long  track width in microns

                    -n long  number of turns

                    -g long  track gap in microns

                    -d long  via drill in mm

                    -l long  length of segment used to approximate circular arc in microns

                    -h prints this

    Example usage:

            python3 src/new_coil.py -o 50000 -w 1270 -v7 -n 5 -g 1270 -d 0.5

            produces a heptagonal coil with 5 turns, 50 mm outer diameter, 1.27 mm track width, 1.27 mm track grap,  0.5 mm via drill

```


# TODO
This repository is still a work in progress, current goals include
- optimizing pinheader placement to take up the least amount of space, regardless of coil shape
    - find and handle all edge cases, especiall for random partial turns & circular coils
    - making the code for finding the optimal coil placement less redundant and more readable (implement method to reuse code instead of copying it multiple times as is currently the case)
- combining approaches/ using a regular circular coil (made of arcs) instead of the one using small lines as approximations in new_coil.py?
- restructuring & dividing code into separate python scripts to make code more readable
- adding support for multiple layers! not just top and bottom Cu layers (this also requires adding the layer as parameter instead of the current hardcode in new_coil.py)
- optimize placement of multiple coils on a 10cm x 10cm PCB board (4 coils, each coil around 5cm x 5cm)
- ensure outer diameter is always adhered to, for all shapes!


# References
a full list of references will be given once the project report is done (it will then be linked here or at least the references)

in the meantime, some of the code was heavily inspired by:
- SpiralInductorFootprintGenerator.java v1.0 Copyright (C) 2015 Erich S. Heinzle, a1039181@gmail.com (https://github.com/erichVK5/SpiralInductorFootprintGenerator)

other references will follow soon