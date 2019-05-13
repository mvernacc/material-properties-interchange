"""Unit tests for Property."""

import unittest
import numpy as np

from materials.property import Property, StateDependentProperty
import materials.variation_with_state as vstate

class TestProperty(unittest.TestCase):
    """Tests for "simple" Property."""
    def test_init(self):
        """Test constructor."""
        yaml_dict = {'default_value': 1.0, 'units': 'MPa', 'reference': 'mmpds'}
        prop = Property('name', yaml_dict)
        self.assertEqual(1.0, prop.default_value)
        self.assertEqual('MPa', prop.units)
        self.assertEqual('mmpds', prop.reference)

    def test_str(self):
        """Test __str__."""
        yaml_dict = {'default_value': 1.0, 'units': 'MPa', 'reference': 'mmpds'}
        prop = Property('Strength', yaml_dict)
        string = str(prop)
        print('\n' + string + '\n')


class TestStateDependentProperty(unittest.TestCase):
    """Tests for StateDependentProperty class."""

    def test_query_1d(self):
        """Test query_value with a 1-d lookup table."""
        # Setup
        dv = 2.0
        yaml_dict = {
            'default_value': dv,
            'units': 'MPa',
            'reference': 'mmpds',
            'variations_with_state': {
                'thermal': {
                    'state_vars': ['temperature'],
                    'state_vars_units': {'temperature': 'kelvin'},
                    'value_type': 'multiplier',
                    'representation': 'table',
                    'reference': 'mmpds',
                    'temperature': np.arange(4),
                    'values': np.arange(4)**2,
                }
            }
        }
        prop = StateDependentProperty('name', yaml_dict)
        model_args_dict = {'method': 'linear'}

        # Action and verification
        # Check queries at given points
        self.assertEqual(prop.query_value({'temperature': 1}), 1**2 * dv)
        self.assertEqual(prop.query_value({'temperature': 2}), 2**2 * dv)
        # Check interpolation between given points
        self.assertAlmostEqual(prop.query_value(
            {'temperature': 2.5}, model_args_dict=model_args_dict), 6.5 * dv)
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
            'variations_with_state': {
                'thermal': {
                    'state_vars': ['exposure time', 'temperature'],
                    'state_vars_units': {'exposure time': 'hour', 'temperature': 'kelvin'},
                    'value_type': 'multiplier',
                    'representation': 'table',
                    'reference': 'mmpds',
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
                }
            }
        }

        # Action
        prop = StateDependentProperty('name', yaml_dict)

        # Verification
        self.assertEqual(2.0, prop.default_value)
        self.assertEqual('MPa', prop.units)
        self.assertEqual('mmpds', prop.reference)
        self.assertEqual(len(prop.variations_with_state['thermal'].state_vars), 2)
        self.assertEqual(prop.variations_with_state['thermal'].state_vars[0], 'exposure time')
        self.assertEqual(prop.variations_with_state['thermal'].state_vars[1], 'temperature')

    def test_query_2d(self):
        """Test query_value with a 2-d lookup table."""
        # Setup
        dv = 2.0
        yaml_dict = {
            'default_value': dv,
            'units': 'MPa',
            'reference': 'mmpds',
            'variations_with_state': {
                'thermal': {
                    'state_vars': ['exposure time', 'temperature'],
                    'state_vars_units': {'exposure time': 'hour', 'temperature': 'kelvin'},
                    'value_type': 'multiplier',
                    'representation': 'table',
                    'reference': 'mmpds',
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
                }
            }}
        model_args_dict = {'method': 'linear'}

        prop = StateDependentProperty('name', yaml_dict)

        # Action and verification
        # Check queries at given points
        result = prop.query_value({'exposure time': 0, 'temperature': 1})
        self.assertEqual(result, 1**2 * dv)
        result = prop.query_value({'exposure time': 0.1, 'temperature': 3})
        self.assertEqual(result, 3.5**2 * dv)
        # Check interpolation between given points
        result = prop.query_value({'exposure time': 0, 'temperature': 2.5},
                                  model_args_dict=model_args_dict)
        self.assertAlmostEqual(result, 6.5 * dv)
        result = prop.query_value({'exposure time': 0.05, 'temperature': 2},
                                  model_args_dict=model_args_dict)
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

    def test_query_1d_eqn(self):
        """Test query_value with a single varaible equation."""
        # Setup
        dv = 2.0
        yaml_dict = {
            'default_value': dv,
            'units': 'MPa',
            'reference': 'mmpds',
            'variations_with_state': {
                'thermal': {
                    'state_vars': ['temperature'],
                    'state_vars_units': {'temperature': 'kelvin'},
                    'value_type': 'multiplier',
                    'representation': 'equation',
                    'reference': 'reference',
                    'expression': 'value = temperature**2',
                    'state_domain': {'temperature': (0, 1000)},
                }
            }
        }
        prop = StateDependentProperty('name', yaml_dict)

        # Action and verification
        # Check good queries
        self.assertEqual(prop.query_value({'temperature': 1}), 1**2 * dv)
        self.assertEqual(prop.query_value({'temperature': 2}), 2**2 * dv)
        # Check bad query
        with self.assertRaises(ValueError):
            prop.query_value({'fish': 1.})    # fish is not a state variable.


    def test_getitem(self):
        """Unit test for __getitem__"""
        # Setup
        dv = 2.0
        yaml_dict = {
            'default_value': dv,
            'units': 'MPa',
            'reference': 'mmpds',
            'variations_with_state': {
                'thermal': {
                    'state_vars': ['temperature'],
                    'state_vars_units': {'temperature': 'kelvin'},
                    'value_type': 'multiplier',
                    'representation': 'table',
                    'reference': 'mmpds',
                    'temperature': np.arange(4),
                    'values': np.arange(4)**2,
                }
            }
        }
        prop = StateDependentProperty('name', yaml_dict)

        # Action
        state_model = prop['thermal']

        # Verification
        self.assertTrue(issubclass(
            type(state_model), vstate.VariationWithState))

    def test_str(self):
        """Unit test for __str__"""
        # Setup
        dv = 2.0
        yaml_dict = {
            'default_value': dv,
            'units': 'MPa',
            'reference': 'mmpds',
            'variations_with_state': {
                'thermal': {
                    'state_vars': ['temperature'],
                    'state_vars_units': {'temperature': 'kelvin'},
                    'value_type': 'multiplier',
                    'representation': 'table',
                    'reference': 'mmpds',
                    'temperature': np.arange(4),
                    'values': np.arange(4)**2,
                }
            }
        }
        prop = StateDependentProperty('Strength', yaml_dict)

        # Action
        string = str(prop)

        # Verification
        print('\n' + string + '\n')



if __name__ == '__main__':
    unittest.main()
