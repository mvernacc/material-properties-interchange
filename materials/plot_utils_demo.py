"""Demonstration of plotting utilities."""
from matplotlib import pyplot as plt

import material
import plot_utils

def main():
    # pylint: disable=no-member
    filename = '../materials_data/Al_6061.yaml'
    al6061 = material.load_from_yaml(filename, 'extruded, thickness > 1 inch', 'T6')

    plot_utils.plot_property_vs_state(al6061.youngs_modulus, 'temperature')

    plt.show()

if __name__ == '__main__':
    main()
