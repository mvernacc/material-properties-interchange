Data Structure Musings
======================

**Work in Progress**

A `material` contains a collection of `properties`. A material may also have other attributes, like a
name, elemental compositon, or category (e.g. metal or plastic).

`properties` are i.e. elastic modulus, yeild strength, density, Poisson's ratio, etc. `properties` have the following attirbutes:
  - name
  - units
  - value
  - A representation of how the value varies with physical state (i.e. temperature).
    This could be a table (e.g. digitized from the plots in MMPDS) or a polynomial (e.g. from NIST).
  - A reference to the source of the data (bibtex?). Traceability is important!

Some properties in MMPDS share a temperature effect representation. How to handle?

Think of `condition` (i.e. heat treatment) as a inheritance structure for materials.
A parent material (e.g. Al 6061) has several child material in different conditions (e.g. -O or -T6).
These childern inherit some properties (e.g. density) but override others (e.g. strength).
