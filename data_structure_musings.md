Data Structure Musings
======================

**Work in Progress**

A `material` contains a collection of `properties`. A material may also have other attributes, like a
name, elemental composition, or category (e.g. metal or plastic).

`properties` are i.e. elastic modulus, yeild strength, density, Poisson's ratio, etc. `properties` have the following attirbutes:
  - name
  - units
  - value
  - Models of how the value varies with physical state (i.e. temperature).
    There may be several models which are appropriate for different contexts, e.g. a model of temperature effects
    for propulsion applications and a model of radiation effects for nuclear applications.
    The model representation could be a table (e.g. digitized from the plots in MMPDS) or a polynomial (e.g. from NIST).
  - A reference to the source of the data (bibtex?). Traceability is important!

Some properties in MMPDS share a temperature effect representation. How to handle? --> YAML `<<: *x` magic

Think of `condition` (i.e. heat treatment) as a inheritance structure for materials.
A parent material (e.g. Al 6061) has several child material in different conditions (e.g. -O or -T6).
These childern inherit some properties (e.g. density) but override others (e.g. strength).
