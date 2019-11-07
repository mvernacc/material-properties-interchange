"""Test to make sure materials in the database load properly."""
import os.path
import unittest
import numpy as np
from materials import Material, load


class TestAISI304(unittest.TestCase):
    """Unit tests for AISI 304."""

    def test_load(self):
        """Make sure the material loads from the YAML file w/o throwing errors."""
        # Action
        aisi304 = load('AISI_304', 'sheet and strip', 'annealed')

        # Verificaiton
        self.assertEqual(type(aisi304), Material)
        # TODO automate checking this
        print('\n' + str(aisi304) + '\n')


class TestAISI316L(unittest.TestCase):
    """Unit tests for AISI 304."""

    def test_load(self):
        """Make sure the material loads from the YAML file w/o throwing errors."""
        # Action
        aisi316L_sheet = load('AISI_316L', 'sheet', 'annealed')
        aisi316L_am_renishaw = load('AISI_316L', 'additive, Renishaw', 'as-built')
        aisi316L_am_eos = load('AISI_316L', 'additive, EOS', 'as-built')

        # Verificaiton
        self.assertEqual(type(aisi316L_sheet), Material)
        self.assertEqual(type(aisi316L_am_renishaw), Material)
        self.assertEqual(type(aisi316L_am_eos), Material)
        # TODO automate checking this
        print('\n' + str(aisi316L_sheet) + '\n')
        print('\n' + str(aisi316L_am_renishaw) + '\n')
        print('\n' + str(aisi316L_am_eos) + '\n')

class TestTi6Al4VELI(unittest.TestCase):
    """Unit tests for Ti-6Al-4V ELI."""
    def test_load(self):
        """Make sure the material loads from the YAML file w/o throwing errors."""
        # Action
        ti64_bar = load('Ti-6Al-4V_ELI', 'bar', 'annealed')
        ti64_am_renishaw = load('Ti-6Al-4V_ELI', 'additive, Renishaw', 'annealed')
        ti64_am_eos = load('Ti-6Al-4V_ELI', 'additive, EOS', 'annealed')

        # Verificaiton
        self.assertEqual(type(ti64_bar), Material)
        self.assertEqual(type(ti64_am_renishaw), Material)
        self.assertEqual(type(ti64_am_eos), Material)
        # TODO automate checking this
        print('\n' + str(ti64_bar) + '\n')
        print('\n' + str(ti64_am_renishaw) + '\n')
        print('\n' + str(ti64_am_eos) + '\n')

class TestIn718(unittest.TestCase):
    """Unit tests for In718."""
    def test_load(self):
        """Make sure the material loads from the YAML file w/o throwing errors."""
        # Action
        in718_bar = load('In718', 'bar', 'solution treated and aged')
        in718_am_renishaw = load('In718', 'additive, Renishaw', 'solution treated and aged')
        in718_am_eos = load('In718', 'additive, EOS', 'solution treated and aged')

        # Verificaiton
        self.assertEqual(type(in718_bar), Material)
        self.assertEqual(type(in718_am_renishaw), Material)
        self.assertEqual(type(in718_am_eos), Material)
        # TODO automate checking this
        print('\n' + str(in718_bar) + '\n')
        print('\n' + str(in718_am_renishaw) + '\n')
        print('\n' + str(in718_am_eos) + '\n')


class TestAlSi10Mg(unittest.TestCase):
    """Unit tests for AlSi10Mg."""
    def test_load(self):
        """Make sure the material loads from the YAML file w/o throwing errors."""
        # Action
        alsi10mg_am_renishaw = load('AlSi10Mg', 'additive, Renishaw', 'stress relieved')

        # Verificaiton
        self.assertEqual(type(alsi10mg_am_renishaw), Material)
        # TODO automate checking this
        print('\n' + str(alsi10mg_am_renishaw) + '\n')


class TestAl6061(unittest.TestCase):
    """Unit tests for Al 6061."""

    def test_load(self):
        """Make sure the material loads from the YAML file w/o throwing errors."""
        # Action
        al6061 = load('Al_6061', 'extruded, thickness > 1 inch', 'T6')

        # Verificaiton
        self.assertEqual(type(al6061), Material)
        # TODO automate checking this
        print('\n' + str(al6061) + '\n')


class TestD6AC(unittest.TestCase):
    """Unit tests for steel D6AC."""

    def test_load(self):
        """Make sure the material loads from the YAML file w/o throwing errors."""
        # Action
        d6ac = load('D6AC', 'bar, forging, tubing', 'tempered to 220 ksi')

        # Verificaiton
        self.assertEqual(type(d6ac), Material)
        # TODO automate checking this
        print('\n' + str(d6ac) + '\n')


if __name__ == '__main__':
    unittest.main()
