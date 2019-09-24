"""Demonstration of plotting utilities."""
import os.path
from matplotlib import pyplot as plt

import materials
from materials import plot_utils


def main():
    al6061 = materials.load('Al_6061', 'extruded, thickness > 1 inch', 'T6')

    axes = plot_utils.plot_property_vs_state(
        al6061.properties['youngs_modulus'], 'thermal', 'temperature')
    plot_utils.decorate_temperature_axis(axes, (50, 800), 'aviation')
    plt.title('Stiffness of {:s} vs. temperature'.format(al6061.name))
    plt.grid()


if __name__ == '__main__':
    main()
    plt.show()
