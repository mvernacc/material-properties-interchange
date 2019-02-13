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

def decorate_temperature_axis(axes, temperature_range=(0, np.inf), comparison_set='space propulsion'):
    """Decorate temperature axis with comparison temperatures.

    References:
        [1] Lozano, Paulo, "Monopropellant Thrusters", 16.522 Notes, MIT.
            Online: https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-522-space-propulsion-spring-2015/lecture-notes/MIT16_522S15_Lecture12.pdf
        [2] Sutton, George P and Oscar Biblarz, Rocket Propulsion Elements, 8th ed., 2010.
    """
    temperature_comparisons = {
        'space propulsion': {
            20.28: 'hydrogen boils',
            90.2: 'oxygen boils',
            111.67: 'methane boils',
            273.15 + 25: 'room temp.',
            1100: 'typ. gas generator',    # see [2], table 5-10.
            1343: 'hydrazine flame',    # Assuming 40% NH3 decomposed, see [1]
            3389: '$H_2 + O_2$ flame'    # Mass oxid/fuel ratio = 5.55, see [2]
        },
        'weather': {
            184: 'Earth record cold',
            273.15: 'water freezes',
            273.15 + 25: 'room temp.',
            273.15 + 70.7: 'Earth record high',
            273.15 + 100: 'water boils',
        }
    }
    annotation_color = (0.3, 0.3, 0.3)

    if comparison_set not in temperature_comparisons:
        raise ValueError(
            '{:s} is not an available temperature comparison set.'
            + 'Available comparison sets:\n'
            + ''.join(['\t{:s}\n'.format(s) for s in temperature_comparisons]))

    for temperature, comparison_text in temperature_comparisons[comparison_set].items():
        if temperature_range[0] < temperature < temperature_range[1]:
            axes.axvline(temperature, color=annotation_color)
            text_y = 0.1 * (axes.get_ylim()[1] - axes.get_ylim()[0]) + axes.get_ylim()[0]
            text_x = temperature
            axes.text(text_x, text_y, comparison_text,
                      rotation=90, color=annotation_color,
                      horizontalalignment='center',
                      verticalalignment='bottom',
                      bbox={'facecolor': 'white', 'alpha': 0.9, 'edgecolor':'none', 'pad': 3})
