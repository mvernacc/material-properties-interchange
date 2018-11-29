Material Properties Interchange
===============================

Do for material properties what STEP files do for 3D geometry.

I've been considering doing this project but haven't had time for it. If you would find it useful please leave a comment or message me. 

# Project Proposal

Provide for the interchange of information on material properties between CAD software, FEA software, and custom analysis scripts.
I spend a lot of time manually transcribing material properties from MAtWeb or MMPDS into SolidWorks and my own python scripts.
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
