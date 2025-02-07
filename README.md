# inductive-coil-design-automation

# TODO
This repository is still a work in progress, current goals include
- optimizing pinheader placement to take up the least amount of space, regardless of coil shape
- enabling fractional turns for all shapes
- combining approaches/ using a regular circular coil (made of arcs) instead of the one using small lines as approximations in new_coil.py?
- restructuring & dividing code into separate python scripts to make code more readable
- add parameter s.t. coils in new_coil.py can be placed wherever (not automatically at 0,0)
- add support for multiple layers! not just top and bottom Cu layers (this also requires adding the layer as parameter instead of the current hardcode in new_coil.py)
- optimize placement of multiple coils on a 10cm x 10cm PCB board (4 coils, each coil around 5cm x 5cm)
- ensure outer diameter is always adhered to, for all shapes!

# References
a full list of references will be given once the project report is done (it will then be linked here or at least the references)

in the meantime, some of the code was heavily inspired by:
- SpiralInductorFootprintGenerator.java v1.0 Copyright (C) 2015 Erich S. Heinzle, a1039181@gmail.com (https://github.com/erichVK5/SpiralInductorFootprintGenerator)

other references will follow soon