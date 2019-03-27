"""Unit tests for Material."""
import os.path
import unittest
import numpy as np
from materials import Material, load_from_yaml, get_database_dir
from material import build_properties
from materials.property import Property


class TestBuildProperties(unittest.TestCase):
    """Unit tests for build_properties."""

    def test_build_properties_simple(self):
        """Test the build properties function with a simple property."""
        # Setup
        yaml_dict = {
            'density': {
                'default_value': 1000.,
                'units': 'kg m^-3',
                'reference': 'mmpds'
                }
            }

        # Action
        properties = build_properties(yaml_dict)

        # Verification
        self.assertTrue('density' in properties)
        self.assertEqual(properties['density'].query_value(), 1000.)
        self.assertEqual(properties['density'].units, 'kg m^-3')

    def test_build_properties_1d_table(self):
        """Test the build properties function with a 1d lookup table."""
        # Setup
        dv = 2.0
        yaml_dict = {
            'strength': {
                'default_value': dv,
                'units': 'MPa',
                'reference': 'mmpds',
                'variations_with_state': {
                    'thermal': {
                        'state_vars': ['temperature'],
                        'state_vars_units': ['kelvin'],
                        'value_type': 'multiplier',
                        'representation': 'table',
                        'reference': 'mmpds',
                        'temperature': np.arange(4),
                        'values': np.arange(4)**2,
                    }
                }
            }
        }

        # Action
        properties = build_properties(yaml_dict)

        # Verification
        self.assertTrue('strength' in properties)
        self.assertEqual(properties['strength'].units, 'MPa')
        result = properties['strength'].query_value({'temperature': 2})
        self.assertEqual(result, 4. * dv)


class TestMaterial(unittest.TestCase):
    """Unit tests for Material class."""

    def test_init(self):
        # Setup
        yaml_dict = {
            'density': {
                'default_value': 1000.,
                'units': 'kg m^-3',
                'reference': 'mmpds'
                }
            }

        # Action
        matl = Material('name', properties_dict=yaml_dict)

        # Verification
        self.assertTrue(hasattr(matl, 'properties'))
        self.assertTrue('density' in matl.properties)
        self.assertEqual(matl.name, 'name')
        self.assertTrue(matl.category is None)

    def test_getitem(self):
        """Unit test for __getitem__"""
        # Setup
        yaml_dict = {
            'density': {
                'default_value': 1000.,
                'units': 'kg m^-3',
                'reference': 'mmpds'
                }
            }
        matl = Material('name', properties_dict=yaml_dict)

        # Action
        prop = matl['density']

        # Verification
        self.assertTrue(issubclass(type(prop), Property))


class TestLoadFromYaml(unittest.TestCase):
    """Unit tests for load_from_yaml."""

    def test_al6061_T6_extruded(self):
        # Setup
        filename = os.path.join(get_database_dir(), 'Al_6061.yaml')

        # Action
        al6061 = load_from_yaml(filename, 'extruded, thickness > 1 inch', 'T6')

        # Verification
        self.assertEqual(al6061.category, 'metal')
        self.assertEqual(al6061.properties['solidus_temperature'].query_value(), 855.)
        self.assertEqual(al6061.properties['youngs_modulus'].units, 'GPa')
        result = al6061.properties['youngs_modulus'].query_value({'temperature': 294})
        self.assertAlmostEqual(result, 68.3, delta=0.5)



if __name__ == '__main__':
    unittest.main()
