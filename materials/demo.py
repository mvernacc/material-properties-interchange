"""Demonstration."""
import os.path
import numpy as np
import matplotlib.pyplot as plt
import materials

def main():
    filename = os.path.join(materials.get_database_dir(), 'Al_6061.yaml')
    al6061 = materials.load_from_yaml(filename, 'extruded, thickness > 1 inch', 'T6')

    temperature = np.linspace(80, 580)
    modulus = al6061.properties['youngs_modulus'].query_value({'temperature': temperature})

    plt.plot(temperature, modulus, label=al6061.name)
    plt.plot(al6061.properties['solidus_temperature'].query_value(), 0, color='C0', marker='x')
    plt.legend()
    plt.grid(True)
    x_units = al6061.properties['youngs_modulus'].state_vars_units[0]
    plt.xlabel('Temperature [{:s}]'.format(x_units))
    y_units = al6061.properties['youngs_modulus'].units
    plt.ylabel('Youngs Modulus $E$ [{:s}]'.format(y_units))

    plt.figure()
    for exp_time in [0.5, 10, 100, 1000, 10000]:    # exposure time [units: hour].
        time = np.full_like(temperature, exp_time)
        uts = al6061.properties['strength_tensile_ultimate'].query_value(
            {'temperature': temperature, 'exposure time': time})

        plt.plot(temperature, uts, label=al6061.name + ', {:.0f} hr exposure'.format(exp_time))
    plt.legend()
    plt.grid(True)
    x_units = al6061.properties['strength_tensile_ultimate'].state_vars_units[0]
    plt.xlabel('Temperature [{:s}]'.format(x_units))
    y_units = al6061.properties['strength_tensile_ultimate'].units
    plt.ylabel('Ultimate Tensile Strength $\\sigma_{{ut}}$ [{:s}]'.format(y_units))


    plt.show()


if __name__ == '__main__':
    main()
