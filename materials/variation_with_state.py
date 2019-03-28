"""Classes for represernting the variaton of material properties with state."""

import numpy as np
import scipy.interpolate


def _create_interp_arrays_from_yaml_table_2d(yaml_dict, state_vars, state_vars_interp_scales):
    """Create 2d interpolation arrays for `griddata` from a YAML dict.

    Arguments:
        yaml_dict (dict): variation with state subdictionary extracted from a YAML file.
        state_vars (list of string): State variable names.
        state_vars_interp_scales (list of string): Interpolation scale for each state
            variable. Should be 'log' or 'linear'.

    Returns:
        ndarray: interpolation points.
        ndarray: interpolation values.
    """
    if len(state_vars) != 2:
        raise ValueError()
    # TODO there has got to be a less awful way to represent a 2+ dimensional
    # interpolation table in YAML and load it.
    interp_points = np.empty((0, 2))
    interp_values = np.array([])
    tbl_dict = yaml_dict[state_vars[0]]
    interp_points_0 = np.array(list(tbl_dict.keys()))
    interp_points_0.sort()
    interp_points_1 = np.array(
        [tbl_dict[p0][state_vars[1]] for p0 in interp_points_0])
    # From the yaml dictionary 2d table, build an array compatible with
    # scipy.interpolate.griddata
    for i in range(len(interp_points_0)):
        # The value of the 0th state variable for this slice of the interpolation table.
        point_0 = interp_points_0[i]
        interp_points = np.append(
            interp_points,
            np.stack(
                (
                    np.full_like(interp_points_1[i], point_0, dtype=np.double),
                    interp_points_1[i]
                ),
                axis=1),
            axis=0)
        interp_values = np.append(interp_values, tbl_dict[point_0]['values'])
    for j in range(2):
        if state_vars_interp_scales[j] == 'log':
            interp_points[:, j] = np.log(interp_points[:, j])

    return interp_points, interp_values


def _create_interp_arrays_from_yaml_table(yaml_dict, state_vars, state_vars_interp_scales):
    """Create 1d or 2d interpolation arrays for `griddata` from a YAML dict.

    Arguments:
        yaml_dict (dict): property dictionary extracted from a YAML file.
        state_vars (list of string): State variable names.
        state_vars_interp_scales (list of string): Interpolation scale for each state
            variable. Should be 'log' or 'linear'.
    Returns:
        ndarray: interpolation points.
        ndarray: interpolation values.
    """
    if len(state_vars) == 1:
        interp_points = np.array(
            yaml_dict[state_vars[0]])
        interp_values = np.array(
            yaml_dict['values'])
        if state_vars_interp_scales[0] == 'log':
            interp_points = np.log(interp_points)
    elif len(state_vars) == 2:
        interp_points, interp_values = _create_interp_arrays_from_yaml_table_2d(
            yaml_dict, state_vars, state_vars_interp_scales)
    else:
        raise NotImplementedError('More than two state variables not supported.')

    return interp_points, interp_values


class VariationWithState:
    """A model of a material property's variation with state."""
    def __init__(self, representation, state_vars, state_vars_units, value_type, reference):
        self.representation = representation
        self.state_vars = state_vars
        self.state_vars_units = state_vars_units
        allowed_value_types = ['multiplier', 'overrride']
        if value_type not in allowed_value_types:
            raise ValueError('Allowed value_types are {}'.format(allowed_value_types))
        self.value_type = value_type
        self.reference = reference

    def query(self, state):
        """Query the variation with state model at a particular state.""" 
        pass

    def get_state_domain(self):
        """Get the domain over which the variation with state model is valid."""
        pass

    def __str__(self):
        state_var_str = ', '.join(self.state_vars)
        domain_str_list = []
        for i, name in enumerate(self.state_vars):
            domain = self.get_state_domain()    #pylint: disable=assignment-from-no-return
            domain_str_list.append(
                '{:.4g} to {:.4g} {:s}'.format(
                    domain[name][0], domain[name][1], self.state_vars_units[i]))
        domain_str = ', '.join(domain_str_list)
        return 'Variation with {:s} over {:s}, represented as a {:s}. [Data from {:s}]'.format(
            state_var_str, domain_str, self.representation, self.reference)


class VariationWithStateTable(VariationWithState):
    """A material property's variation with state, represented as a table."""
    def __init__(self, state_vars, state_vars_units, value_type, reference,
                 interp_points, interp_values, state_vars_interp_scales):
        VariationWithState.__init__(self, 'table', state_vars, state_vars_units, value_type, reference)
        self._interp_points = interp_points
        self._interp_values = interp_values
        self._state_vars_interp_scales = state_vars_interp_scales

    def query_value(self, state, method='linear', fill_value=np.nan, rescale=True):
        """Query the value of the property at a particular state.

        Arguments:
            state (dict): TODO

        Returns:
            scalar: value of the property at the provided state.
        """
        # Check that all the state variables have been provided in `state`.
        for var_name in self.state_vars:
            if var_name not in state.keys():
                raise ValueError('{:s} not provided for query'.format(var_name))

        # Form an array of points at which to query the interpolation.
        if len(self.state_vars) == 1:
            query_points = np.array(state[self.state_vars[0]])
            if self._state_vars_interp_scales[0] == 'log':
                query_points = np.log(query_points)
        elif len(self.state_vars) == 2:
            if hasattr(state[self.state_vars[0]], '__len__') \
            and hasattr(state[self.state_vars[1]], '__len__'):
                assert len(state[self.state_vars[0]]) == len(state[self.state_vars[1]])
                query_points = np.stack(
                    (state[self.state_vars[0]], state[self.state_vars[1]]), axis=1)
            else:
                query_points = np.array([[state[self.state_vars[0]], state[self.state_vars[1]]]])

            # If one of the state variables is interpolated on a log scale,
            # take its log in the query.
            for j in range(len(self.state_vars)):
                if self._state_vars_interp_scales[j] == 'log':
                    query_points[:, j] = np.log(query_points[:, j])

        values = scipy.interpolate.griddata(self._interp_points, self._interp_values,
                                            query_points,
                                            method=method, fill_value=fill_value, rescale=rescale)

        return values

    def get_state_domain(self):
        """Get the domain over which the property's variation with state model is valid.

        Returns:
            dict: each key is the name of a state variable.
            Values are tuples `(smin, smax)` where `smin` is the minimum bound
            of the valid domain in that state variable and `smax` is the maximum bound.
            The units of `smin` and `smax` are given by `state_vars_units[key]`.
        """
        if len(self.state_vars) == 1:
            # Assumes interpolation points are in ascending order.
            smin = self._interp_points[0]
            smax = self._interp_points[-1]
            if self._state_vars_interp_scales[0] == 'log':
                smin = np.exp(smin)
                smax = np.exp(smax)
            result = {self.state_vars[0]: (smin, smax)}
        elif len(self.state_vars) == 2:
            result = {}
            for j in range(2):
                # Assumes interpolation points are in ascending order.
                smin = self._interp_points[0, j]
                smax = self._interp_points[-1, j]
                if self._state_vars_interp_scales[j] == 'log':
                    smin = np.exp(smin)
                    smax = np.exp(smax)
                result[self.state_vars[j]] = (smin, smax)
        return result


def build_from_yaml(yaml_dict):
    """Construct a variation with state object from a YAML-derived dictionary."""
    state_vars = yaml_dict['state_vars']
    state_vars_units = yaml_dict['state_vars_units']
    value_type = yaml_dict['value_type']
    reference = yaml_dict['reference']

    if yaml_dict['representation'] == 'table':
        state_vars_interp_scales = yaml_dict.get(
            'state_vars_interp_scales', ['linear'] * len(state_vars))
        interp_points, interp_values = _create_interp_arrays_from_yaml_table(
            yaml_dict, state_vars, state_vars_interp_scales)
        return VariationWithStateTable(
            state_vars, state_vars_units, value_type, reference,
            interp_points, interp_values, state_vars_interp_scales)
    else:
        raise NotImplementedError('Representations other than table are not yet supported.')