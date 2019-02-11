"""Unit tests for Property."""

import unittest
import numpy as np

from property import Property, StateDependentProperty

class TestProperty(unittest.TestCase):
    """Tests for "simple" Property."""
    def test_init(self):
        """Test constructor."""
        yaml_dict = {'default_value': 1.0, 'units': 'MPa', 'reference': 'mmpds'}
        prop = Property(yaml_dict)
        self.assertEqual(1.0, prop.default_value)
        self.assertEqual('MPa', prop.units)
        self.assertEqual('mmpds', prop.reference)


class TestStateDependentProperty(unittest.TestCase):
    """Tests for StateDependentProperty class."""
    def test_init_1d(self):
        """Test init with a 1-d lookup table."""
        # Setup
        yaml_dict = {
            'default_value': 2.0,
            'units': 'MPa',
            'reference': 'mmpds',
            'variation_with_state': {
                'state_vars': ['temperature'],
                'value_type': 'multiplier',
                'representation': 'table',
                'temperature': np.arange(4),
                'values': np.arange(4)**2,
            }}

        # Action
        prop = StateDependentProperty(yaml_dict)

        # Verification
        self.assertEqual(2.0, prop.default_value)
        self.assertEqual('MPa', prop.units)
        self.assertEqual('mmpds', prop.reference)
        self.assertEqual(len(prop.state_vars), 1)
        self.assertEqual(prop.state_vars[0], 'temperature')

    def test_query_1d(self):
        """Test query_value with a 1-d lookup table."""
        # Setup
        dv = 2.0
        yaml_dict = {
            'default_value': dv,
            'units': 'MPa',
            'reference': 'mmpds',
            'variation_with_state': {
                'state_vars': ['temperature'],
                'value_type': 'multiplier',
                'representation': 'table',
                'temperature': np.arange(4),
                'values': np.arange(4)**2,
            }}
        prop = StateDependentProperty(yaml_dict)

        # Action and verification
        # Check queries at given points
        self.assertEqual(prop.query_value({'temperature': 1}), 1**2 * dv)
        self.assertEqual(prop.query_value({'temperature': 2}), 2**2 * dv)
        # Check interpolation between given points
        self.assertAlmostEqual(prop.query_value({'temperature': 2.5}, method='linear'), 6.5 * dv)
        # Check bad query
        with self.assertRaises(ValueError):
            prop.query_value({'fish': 1.})    # fish is not a state variable.



if __name__ == '__main__':
    unittest.main()
