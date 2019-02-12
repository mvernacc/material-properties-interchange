"""classes for representing and quesrying properties of a material."""
import numpy as np
import scipy.interpolate

class Property:
    """A property of a material."""
    def __init__(self, yaml_dict):
        self.default_value = yaml_dict['default_value']
        self.units = yaml_dict['units']
        self.reference = yaml_dict['reference']


class StateDependentProperty(Property):
    """A property of a material which depends on state (e.g. temperature)."""
    def __init__(self, yaml_dict):
        Property.__init__(self, yaml_dict)
        self.state_vars = yaml_dict['variation_with_state']['state_vars']
        self._value_type = yaml_dict['variation_with_state']['value_type']
        self._representation = yaml_dict['variation_with_state']['representation']

        if self._representation == 'table':
            if len(self.state_vars) == 1:
                self._interp_points = np.array(
                    yaml_dict['variation_with_state'][self.state_vars[0]])
                self._interp_values = np.array(
                    yaml_dict['variation_with_state']['values'])
            elif len(self.state_vars) == 2:
                # TODO there has got to be a less awful way to represent a 2+ dimensional
                # interpolation table in YAML and load it.
                self._interp_points = np.empty((0, 2))
                self._interp_values = np.array([])
                tbl_dict = yaml_dict['variation_with_state'][self.state_vars[0]]
                interp_points_0 = np.array(list(tbl_dict.keys()))
                interp_points_0.sort()
                interp_points_1 = np.array(
                    [tbl_dict[p0][self.state_vars[1]] for p0 in interp_points_0])
                # From the yaml dictionary 2d table, build an array compatible with
                # scipy.interpolate.griddata
                for i in range(len(interp_points_0)):
                    # The value of the 0th state variable for this slice of the inperpolation table.
                    point_0 = interp_points_0[i]
                    self._interp_points = np.append(
                        self._interp_points,
                        np.stack(
                            (
                                np.full_like(interp_points_1[i], point_0, dtype=np.double),
                                interp_points_1[i]
                            ),
                            axis=1),
                        axis=0)
                    self._interp_values = np.append(self._interp_values, tbl_dict[point_0]['values'])
            else:
                raise NotImplementedError('More than two state variables not supported.')

        else:
            raise NotImplementedError('Representations other than table are not yet supported.')


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
        elif len(self.state_vars) == 2:
            if hasattr(state[self.state_vars[0]], '__len__') \
            and hasattr(state[self.state_vars[1]], '__len__'):
                assert len(state[self.state_vars[0]]) == len(state[self.state_vars[1]])
                query_points = np.stack(
                    (state[self.state_vars[0]], state[self.state_vars[1]]), axis=1)
            else:
                query_points = np.array([[state[self.state_vars[0]], state[self.state_vars[1]]]])

        values = scipy.interpolate.griddata(self._interp_points, self._interp_values,
                                            query_points,
                                            method=method, fill_value=fill_value, rescale=rescale)

        if self._value_type == 'multiplier':
            values = self.default_value * values

        return values
