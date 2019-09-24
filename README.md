Material Properties Interchange
===============================
[![Build Status](https://travis-ci.org/mvernacc/material-properties-interchange.svg?branch=master)](https://travis-ci.org/mvernacc/material-properties-interchange) [![codecov](https://codecov.io/gh/mvernacc/material-properties-interchange/branch/master/graph/badge.svg)](https://codecov.io/gh/mvernacc/material-properties-interchange)



Do for material properties what STEP files do for 3D geometry.

I've only made a rough demo so far. If you would find it useful please leave a comment or message me.

# Current Status
Check out `tutorials/xplane_airframes.ipynb` for a demonstration of how to use the package and why it's useful for engineers.

So far, I've implemented the following:
  -  A prototype of a material database record in YAML: `materials_data/Al_6061.yaml`. So far this is only a limited subset of properties for a single material.
  - The core datastructures + logic for representing a material property, and doing interpolation for state-dependent properties: `materials/property.py`.
  - The core logic for loading material data from a YAMl file into a python object: `materials/material.py`.
  -  Some unit tests for the above.

# Project Proposal

Provide for the interchange of information on material properties between CAD software, FEA software, and custom analysis scripts.
I spend a lot of time manually transcribing material properties from MatWeb or MMPDS into SolidWorks and my own python scripts.
This process is tedious and error prone -  I'd like to make it better, and I imagine other engineers would appreciate this too.
It would be valuable for a project to have a single (verified) database of material properties, which all of the project's computational tools (CAD, FEA, analysis scripts) reference.

## Core components

### Database
Format for recording properties of a material. Use a standard syntax (YAML)?

### Interchange Programs
Import from MatWeb.

Convert to/from formats used by major CAD/FEA packages.

### API
Access material properties from python, MATLAB, Excel(?).


# Similar Products/Projects

[Granta MI](https://www.grantadesign.com/products/mi/) and the [Material Data Management Consortium](http://www.grantadesign.com/download/pdf/mdmc_datasheet.pdf)
