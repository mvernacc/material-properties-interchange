import os.path
import numpy as np
import matplotlib.pyplot as plt
import materials
from materials import plot_utils

def main():
    # Load copper properties from the data file
    filename = os.path.join(materials.get_database_dir(), 'copper.yaml')
    copper = materials.load_from_yaml(filename, 'wire', 'annealed')

    # Print a summary of the available properties for copper
    print(copper)

    # Query the heat capacity
    cp_300 = copper['heat_capacity'].query_value({'temperature': 300})
    print('Heat capacity of copper at 300 K = {:.1f} {:s}'.format(
        cp_300, copper['heat_capacity'].units))

    # Query the resistivity at several temperatures
    temp = np.linspace(100, 600, 6)
    rho = copper['electrical_resistivity'].query_value({'temperature': temp})
    print('Electrical resistivity of copper:')
    print('temperature: ' + str(temp) + ' K')
    print('resistivity: ' + str(rho) + copper['electrical_resistivity'].units)

    # Make plots
    plt.figure(figsize=(6, 8))
    ax1 = plt.subplot(2, 1, 1)
    plot_utils.plot_property_vs_state(
        copper['electrical_resistivity'], 'thermal', 'temperature', axes=ax1)
    ax2 = plt.subplot(2, 1, 2, sharex=ax1)
    plot_utils.plot_property_vs_state(
        copper['heat_capacity'], 'thermal', 'temperature', axes=ax2)

    plt.suptitle('Electrical resistivity and heat capacity of pure copper')
    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.show()

if __name__ == '__main__':
    main()
