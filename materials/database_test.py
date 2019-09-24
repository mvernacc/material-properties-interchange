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


if __name__ == '__main__':
    unittest.main()
