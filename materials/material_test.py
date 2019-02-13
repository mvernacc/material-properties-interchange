"""Unit tests for Material."""
import unittest
import numpy as np
from material import Material, load_from_yaml

class TestMaterial(unittest.TestCase):

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
        matl = Material('name')
        matl.build_properties(yaml_dict)

        # Verification
        self.assertTrue(hasattr(matl, 'density'))
        self.assertEqual(matl.density.query_value(), 1000.)
        self.assertEqual(matl.density.units, 'kg m^-3')

    def test_build_properties_1d_table(self):
        """Test the build properties function with a 1d lookup table."""
        # Setup
        dv = 2.0
        yaml_dict = {
            'strength': {
                'default_value': dv,
                'units': 'MPa',
                'reference': 'mmpds',
                'variation_with_state': {
                    'state_vars': ['temperature'],
                    'state_vars_units': ['kelvin'],
                    'value_type': 'multiplier',
                    'representation': 'table',
                    'temperature': np.arange(4),
                    'values': np.arange(4)**2,
                }
            }
        }

        # Action
        matl = Material('name')
        matl.build_properties(yaml_dict)

        # Verification
        self.assertTrue(hasattr(matl, 'strength'))
        self.assertEqual(matl.strength.units, 'MPa')
        result = matl.strength.query_value({'temperature': 2})
        self.assertEqual(result, 4. * dv)


class TestLoadFromYaml(unittest.TestCase):
    """Unit tests for load_from_yaml."""

    def test_al6061_T6_extruded(self):
        # Setup
        filename = '../materials_data/Al_6061.yaml'

        # Action
        al6061 = load_from_yaml(filename, 'extruded, thickness > 1 inch', 'T6')

        # Verification
        self.assertEqual(al6061.category, 'metal')
        self.assertEqual(al6061.solidus_temperature.query_value(), 855.)
        self.assertEqual(al6061.youngs_modulus.units, 'GPa')
        result = al6061.youngs_modulus.query_value({'temperature': 294})
        self.assertAlmostEqual(result, 68.3, delta=0.5)



if __name__ == '__main__':
    unittest.main()
