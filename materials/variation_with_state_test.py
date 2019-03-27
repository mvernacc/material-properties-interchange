"""Unit tests for variation_woth_state."""

import unittest
import numpy as np

import materials.variation_with_state as vstate


class TestCreatInterpArrays(unittest.TestCase):
    """Tests for _create_interp_arrays_from_yaml_table."""

    def test_2d(self):
        """Test with a 2-d lookup table."""
        # Setup
        yaml_dict = {
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
        }

        # Action
        #pylint: disable=protected-access
        interp_points, interp_values = vstate._create_interp_arrays_from_yaml_table(
            yaml_dict, yaml_dict['state_vars'], ['linear', 'linear'])

        # Verification
        self.assertEqual(interp_points.shape[0], 4 * 2)
        self.assertEqual(interp_points.shape[1], 2)
        self.assertEqual(interp_points[0, 0], 0)
        self.assertEqual(interp_points[4, 0], 0.1)
        self.assertEqual(interp_points[0, 1], 0)
        self.assertEqual(interp_points[3, 1], 3)
        self.assertEqual(interp_points[4, 1], 0)
        self.assertEqual(interp_points[7, 1], 3)

        self.assertEqual(len(interp_values.shape), 1)
        self.assertEqual(interp_values.shape[0], 4 * 2)
        self.assertEqual(interp_values[0], 0)
        self.assertEqual(interp_values[3], 3**2)
        self.assertEqual(interp_values[4], 0.1**2)
        self.assertEqual(interp_values[7], (3.1)**2)


class TestBuildFromYaml(unittest.TestCase):
    """Unit tests for build_from_yaml."""

    def test_build_table_1d(self):
        """Test build_from_yaml with a 1-d lookup table."""
        # Setup
        yaml_dict = {
            'state_vars': ['temperature'],
            'state_vars_units': ['kelvin'],
            'value_type': 'multiplier',
            'representation': 'table',
            'reference': 'mmpds',
            'temperature': np.arange(4),
            'values': np.arange(4)**2,
            }

        # Action
        state_model = vstate.build_from_yaml(yaml_dict)

        # Verification
        self.assertEqual('mmpds', state_model.reference)
        self.assertEqual(len(state_model.state_vars), 1)
        self.assertEqual(state_model.state_vars[0], 'temperature')

    def test_build_table_2d(self):
        """Test build_from_yaml with a 2-d lookup table."""
        # Setup
        yaml_dict = {
            'state_vars': ['exposure time', 'temperature'],
            'state_vars_units': ['hour', 'kelvin'],
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

        # Action
        state_model = vstate.build_from_yaml(yaml_dict)

        # Verification
        self.assertEqual('mmpds', state_model.reference)
        self.assertEqual(len(state_model.state_vars), 2)
        self.assertEqual(state_model.state_vars[0], 'exposure time')
        self.assertEqual(state_model.state_vars[1], 'temperature')


class TestVariationWithStateTable(unittest.TestCase):
    """Unit tests for VariationWithStateTable."""

    def test_query_1d(self):
        """Test queries on a 1-d lookup table."""
        # Setup
        state_model = vstate.VariationWithStateTable(
            ['temperature'], ['kelvin'], 'multiplier', 'reference',
            np.arange(4), np.arange(4)**2,
            ['linear'])

        # Action and verification
        # Check queries at given points
        self.assertEqual(state_model.query_value({'temperature': 1}), 1**2)
        self.assertEqual(state_model.query_value({'temperature': 2}), 2**2)
        # Check interpolation between given points
        self.assertAlmostEqual(state_model.query_value({'temperature': 2.5}, method='linear'), 6.5)
        # Check bad query
        with self.assertRaises(ValueError):
            state_model.query_value({'fish': 1.})    # fish is not a state variable.

    def test_query_2d(self):
        """Test queries on a 2-d lookup table."""
        # Setup
        yaml_dict = {
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
        state_vars = ['exposure time', 'temperature']
        scales = ['linear', 'linear']
        #pylint: disable=protected-access
        interp_points, interp_values = vstate._create_interp_arrays_from_yaml_table(
            yaml_dict, state_vars, scales)

        state_model = vstate.VariationWithStateTable(
            state_vars, ['hour', 'kelvin'], 'multiplier', 'reference',
            interp_points, interp_values,
            scales)

        # Action and verification
        # Check queries at given points
        result = state_model.query_value({'exposure time': 0, 'temperature': 1})
        self.assertEqual(result, 1**2)
        result = state_model.query_value({'exposure time': 0.1, 'temperature': 3})
        self.assertEqual(result, 3.5**2)
        # Check interpolation between given points
        result = state_model.query_value({'exposure time': 0, 'temperature': 2.5}, method='linear')
        self.assertAlmostEqual(result, 6.5)
        result = state_model.query_value({'exposure time': 0.05, 'temperature': 2}, method='linear')
        self.assertAlmostEqual(result, (2**2 + 2.5**2)/2)

        # Check query of multiple points
        result = state_model.query_value({'exposure time': [0, 0.05], 'temperature': [1, 2]})
        self.assertEqual(result[0], 1**2)
        self.assertAlmostEqual(result[1], (2**2 + 2.5**2)/2)

        # Check bad query
        with self.assertRaises(ValueError):
            # fish is not a state variable.
            state_model.query_value({'fish': 1., 'temperature': 1})
        with self.assertRaises(ValueError):
            # fish is not a state variable.
            state_model.query_value({'fish': 1., 'exposure time': 1})

    def test_domain_1d(self):
        """Test get_state_domain on a 1-d lookup table."""
        # Setup
        state_model = vstate.VariationWithStateTable(
            ['temperature'], ['kelvin'], 'multiplier', 'reference',
            np.arange(4), np.arange(4)**2,
            ['linear'])

        # Action
        domain = state_model.get_state_domain()

        # Verification
        self.assertEqual(len(domain), 1)
        self.assertTrue('temperature' in domain)
        self.assertEqual(domain['temperature'][0], 0)
        self.assertEqual(domain['temperature'][1], 3)


    def test_domain_2d(self):
        """Test get_state_domain on a 2-d lookup table."""
        # Setup
        yaml_dict = {
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
        state_vars = ['exposure time', 'temperature']
        scales = ['linear', 'linear']
        #pylint: disable=protected-access
        interp_points, interp_values = vstate._create_interp_arrays_from_yaml_table(
            yaml_dict, state_vars, scales)

        state_model = vstate.VariationWithStateTable(
            state_vars, ['hour', 'kelvin'], 'multiplier', 'reference',
            interp_points, interp_values,
            scales)

        # Action
        domain = state_model.get_state_domain()

        # Verification
        self.assertEqual(len(domain), 2)
        self.assertTrue('exposure time' in domain)
        self.assertTrue('temperature' in domain)
        self.assertEqual(domain['exposure time'][0], 0.0)
        self.assertEqual(domain['exposure time'][1], 0.1)
        self.assertEqual(domain['temperature'][0], 0)
        self.assertEqual(domain['temperature'][1], 3)

    def test_str(self):
        """Unit test for __str__."""
        # Setup
        yaml_dict = {
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
        state_vars = ['exposure time', 'temperature']
        scales = ['linear', 'linear']
        #pylint: disable=protected-access
        interp_points, interp_values = vstate._create_interp_arrays_from_yaml_table(
            yaml_dict, state_vars, scales)

        state_model = vstate.VariationWithStateTable(
            state_vars, ['hour', 'kelvin'], 'multiplier', 'reference',
            interp_points, interp_values,
            scales)

        # Action
        string = str(state_model)

        # Verification
        # TODO automate checking this?
        print(string)


if __name__ == '__main__':
    unittest.main()
