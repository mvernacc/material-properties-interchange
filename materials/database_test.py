"""Test to make sure materials in the database load properly."""
import os.path
import unittest
import numpy as np
from materials import Material, load_from_yaml, get_database_dir


class TestAISI304(unittest.TestCase):
    """Unit tests for AISI 304."""

    def test_load(self):
        """Make sure the material loads from the YAML file w/o throwing errors."""
        # Setup
        filename = os.path.join(get_database_dir(), 'AISI_304.yaml')

        # Action
        asis304 = load_from_yaml(filename, 'sheet and strip', 'annealed')

        # Verificaiton
        self.assertEqual(type(asis304), Material)
        # TODO automate checking this
        print('\n' + str(asis304) + '\n')


class TestAl6061(unittest.TestCase):
    """Unit tests for Al 6061."""

    def test_load(self):
        """Make sure the material loads from the YAML file w/o throwing errors."""
        # Setup
        filename = os.path.join(get_database_dir(), 'Al_6061.yaml')

        # Action
        al6061 = load_from_yaml(filename, 'extruded, thickness > 1 inch', 'T6')

        # Verificaiton
        self.assertEqual(type(al6061), Material)
        # TODO automate checking this
        print('\n' + str(al6061) + '\n')


if __name__ == '__main__':
    unittest.main()
