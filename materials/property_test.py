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
                'state_vars_units': ['kelvin'],
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
                'state_vars_units': ['kelvin'],
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

    def test_init_2d(self):
        """Test init with a 2-d lookup table."""
        # Setup
        yaml_dict = {
            'default_value': 2.0,
            'units': 'MPa',
            'reference': 'mmpds',
            'variation_with_state': {
                'state_vars': ['exposure time', 'temperature'],
                'state_vars_units': ['hour', 'kelvin'],
                'value_type': 'multiplier',
                'representation': 'table',
                'exposure time': {
                    0.0: {
                        'temperature': np.arange(4),
                        'values': np.arange(4)**2
                    },
                    0.1: {
                        'temperature': np.arange(4),
                        'values': (np.arange(4) + 0.1)**2
                    },
                }
            }}

        # Action
        prop = StateDependentProperty(yaml_dict)

        # Verification
        self.assertEqual(2.0, prop.default_value)
        self.assertEqual('MPa', prop.units)
        self.assertEqual('mmpds', prop.reference)
        self.assertEqual(len(prop.state_vars), 2)
        self.assertEqual(prop.state_vars[0], 'exposure time')
        self.assertEqual(prop.state_vars[1], 'temperature')

        # Verification of "private" attributes
        # These tests are tied to the implementation, not interface
        # Is this sketchy? Should the test only depend on the interface?
        # pylint: disable=protected-access
        self.assertEqual(prop._interp_points.shape[0], 4 * 2)
        self.assertEqual(prop._interp_points.shape[1], 2)
        self.assertEqual(prop._interp_points[0, 0], 0)
        self.assertEqual(prop._interp_points[4, 0], 0.1)
        self.assertEqual(prop._interp_points[0, 1], 0)
        self.assertEqual(prop._interp_points[3, 1], 3)
        self.assertEqual(prop._interp_points[4, 1], 0)
        self.assertEqual(prop._interp_points[7, 1], 3)

    def test_query_2d(self):
        """Test query_value with a 2-d lookup table."""
        # Setup
        dv = 2.0
        yaml_dict = {
            'default_value': dv,
            'units': 'MPa',
            'reference': 'mmpds',
            'variation_with_state': {
                'state_vars': ['exposure time', 'temperature'],
                'state_vars_units': ['hour', 'kelvin'],
                'value_type': 'multiplier',
                'representation': 'table',
                'exposure time': {
                    0.0: {
                        'temperature': np.arange(4),
                        'values': np.arange(4)**2
                    },
                    0.1: {
                        'temperature': np.arange(4),
                        'values': (np.arange(4) + 0.5)**2
                    },
                }
            }}

        prop = StateDependentProperty(yaml_dict)

        # Action and verification
        # Check queries at given points
        result = prop.query_value({'exposure time': 0, 'temperature': 1})
        self.assertEqual(result, 1**2 * dv)
        result = prop.query_value({'exposure time': 0.1, 'temperature': 3})
        self.assertEqual(result, 3.5**2 * dv)
        # Check interpolation between given points
        result = prop.query_value({'exposure time': 0, 'temperature': 2.5}, method='linear')
        self.assertAlmostEqual(result, 6.5 * dv)
        result = prop.query_value({'exposure time': 0.05, 'temperature': 2}, method='linear')
        self.assertAlmostEqual(result, (2**2 + 2.5**2)/2 * dv)

        # Check query of multiple points
        result = prop.query_value({'exposure time': [0, 0.05], 'temperature': [1, 2]})
        self.assertEqual(result[0], 1**2 * dv)
        self.assertAlmostEqual(result[1], (2**2 + 2.5**2)/2 * dv)

        # Check bad query
        with self.assertRaises(ValueError):
            prop.query_value({'fish': 1., 'temperature': 1})    # fish is not a state variable.
        with self.assertRaises(ValueError):
            prop.query_value({'fish': 1., 'exposure time': 1})    # fish is not a state variable.



if __name__ == '__main__':
    unittest.main()
