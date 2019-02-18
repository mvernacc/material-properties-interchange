"""Demonstration of plotting utilities."""
import os.path
from matplotlib import pyplot as plt

import materials
from materials import plot_utils

def main():
    filename = os.path.join(materials.get_database_dir(), 'Al_6061.yaml')
    al6061 = materials.load_from_yaml(filename, 'extruded, thickness > 1 inch', 'T6')

    axes = plot_utils.plot_property_vs_state(al6061.properties['youngs_modulus'], 'temperature')
    plot_utils.decorate_temperature_axis(axes, (50, 800), 'aviation')
    plt.grid()

    plt.show()

if __name__ == '__main__':
    main()
