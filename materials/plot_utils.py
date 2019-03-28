"""Material Property plotting utilities."""

import numpy as np
from matplotlib import pyplot as plt


def plot_property_vs_state(prop, state_model=None, state_name=None, state_range=None,
                           value_for_other_state=None, axes=None, **pyplot_kwargs):
    """Plot a state-dependent property.

    Arguments:
        prop (Property): The property to plot.
        state_model (string): The name of the state model to plot from (i.e. a key of `variations_with_state`)
        state_name (string): Name of the state variable to plot the property value against.
        state_range (tuple of length 2): Range of state variable values to plot over (low, high).
        value_for_other_state (scalar): If the property depends on two states, fix the
            other state at this value.
        axes (matplotlib.axes.Axes): Axes to plot on. Makes a new figure if `axes` is None.

    Other keyword arguments are passed to `pyplot.plot`.

    Returns:
        matplotlib.axes.Axes: The axes on which the plot was drawn.
    """
    if state_model is None:
        state_model = prop.default_state_model
    if state_model not in prop.variations_with_state:
        raise ValueError('Property {:s} does not have a variation with state model named {:s}'.format(
            prop.name, state_model))
    if state_name is None:
        state_name = prop.variations_with_state[state_model].state_vars[0]
    if len(prop.variations_with_state[state_model].state_vars) > 1 and value_for_other_state is None:
        raise ValueError('Property depends on more than one state. Must provide value_for_other_state.')
    if len(prop.variations_with_state[state_model].state_vars) == 1 and value_for_other_state is not None:
        raise ValueError('Property only depends on one state, do not provide value_for_other_state.')

    if state_name not in prop.variations_with_state[state_model].state_vars:
        raise ValueError('Property does not have a state variable named {:s}'.format(state_name))

    if state_range is None:
        state_range = prop.variations_with_state[state_model].get_state_domain()[state_name]

    if axes is None:
        plt.figure()
        axes = plt.axes()

    states = np.linspace(state_range[0], state_range[1])
    query = {state_name: states}
    if value_for_other_state is not None:
        other_state_name = (set(prop.state_vars) - set((state_name,))).pop()
        query[other_state_name] = np.full_like(states, value_for_other_state)

    values = prop.query_value(query, state_model)

    axes.plot(states, values, **pyplot_kwargs)

    index = prop.variations_with_state[state_model].state_vars.index(state_name)
    axes.set_xlabel('{:s} [{:s}]'.format(
        state_name, prop.variations_with_state[state_model].state_vars_units[index]))
    axes.set_ylabel('{:s} [{:s}]'.format(
        prop.name.replace('_', ' '), prop.units))

    return axes


def decorate_temperature_axis(axes, temperature_range=(0, np.inf), comparison_set='space propulsion'):
    """Decorate temperature axis with comparison temperatures.

    References:
        [1] Lozano, Paulo, "Monopropellant Thrusters", 16.522 Notes, MIT.
            Online: https://ocw.mit.edu/courses/aeronautics-and-astronautics/16-522-space-propulsion-spring-2015/lecture-notes/MIT16_522S15_Lecture12.pdf
        [2] Sutton, George P and Oscar Biblarz, Rocket Propulsion Elements, 8th ed., 2010.
        [3] US Department of Defense, "Global Climatic Data for Developing Military Products", MIL-HDBK-310, 1997.
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
        },
        'aviation': {
            199: 'cold day, 10 km alt.',    # 1% cold day, see [3] table 5.3.2.2.2
            273.15 + 25: 'room temp.',
            273.15 + 49: 'hot day, desert',    # 1% hot day, Saharah desert, see [3] sec. 5.1.1.2
            278 * (1 + 0.2 * 2**2): '$T_{stag}$ at Mach 2',   # 1% hot day at 5 km alt, see [3]
            278 * (1 + 0.2 * 3**2): '$T_{stag}$ at Mach 3',
            278 * (1 + 0.2 * 4**2): '$T_{stag}$ at Mach 4',
            278 * (1 + 0.2 * 5**2): '$T_{stag}$ at Mach 5',
            278 * (1 + 0.2 * 6**2): '$T_{stag}$ at Mach 6',
            273.15 + 2093: 'kerosene + air flame',
        }
    }
    annotation_color = (0.4, 0.4, 0.4)

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
