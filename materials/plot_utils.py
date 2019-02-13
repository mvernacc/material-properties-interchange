"""Material Property plotting utilities."""

import numpy as np
from matplotlib import pyplot as plt


def plot_property_vs_state(prop, state_name, state_range=None,
                           value_for_other_state=None, axes=None, **kwargs):
    """Plot a state-dependent property."""
    if len(prop.state_vars) > 1 and value_for_other_state is None:
        raise ValueError('Property depends on more than one state. Must provide value_for_other_state.')
    if len(prop.state_vars) == 1 and value_for_other_state is not None:
        raise ValueError('Property only depends on one state, do not provide value_for_other_state.')

    if state_name not in prop.state_vars:
        raise ValueError('Property does not have a state avriable named {:s}'.format(state_name))

    if state_range is None:
        state_range = prop.get_state_domain()[state_name]

    if axes is None:
        plt.figure()
        axes = plt.axes()

    states = np.linspace(state_range[0], state_range[1])
    query = {state_name: states}
    if value_for_other_state is not None:
        other_state_name = (set(prop.state_vars) - set((state_name,))).pop()
        query[other_state_name] = np.full_like(states, value_for_other_state)

    values = prop.query_value(query)

    axes.plot(states, values, **kwargs)

    index = prop.state_vars.index(state_name)
    axes.set_xlabel('{:s} [{:s}]'.format(state_name, prop.state_vars_units[index]))
    axes.set_ylabel('{:s} [{:s}]'.format(prop.name.replace('_', ' '), prop.units))

    return axes
