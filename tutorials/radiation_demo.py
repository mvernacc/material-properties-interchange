import os.path
import numpy as np
import matplotlib.pyplot as plt
import materials

def main():
    filename = os.path.join(materials.get_database_dir(), 'AISI_304.yaml')
    aisi304 = materials.load_from_yaml(filename, 'sheet and strip', 'annealed')

    fig, axes = plt.subplots(nrows=2, ncols=2, sharex='col', sharey='row', figsize=(10, 6))

    dose = np.logspace(19.5, 22)
    temperatures = np.array([300, 300+273, 600+273, 700+273, 1023])
    colors = plt.cm.hot(np.linspace(0, 0.5, len(temperatures)))
    for (temp, color) in zip(temperatures, colors):
        yts = aisi304['strength_tensile_yield'].query_value(
            {'temperature': temp, 'neutron dose': dose}, 'radiation')
        elong = aisi304['elongation'].query_value(
            {'temperature': temp, 'neutron dose': dose}, 'radiation')
        axes[0, 0].semilogx(dose, yts, label='$T={:.0f}$ K'.format(temp), color=color)
        axes[1, 0].semilogx(dose, elong, label='$T={:.0f}$ K'.format(temp), color=color)
    xunits = aisi304['strength_tensile_yield']['radiation'].state_vars_units['neutron dose']
    yunits = aisi304['strength_tensile_yield'].units
    axes[0, 0].set_ylabel('Yield tensile strength [{:s}]'.format(yunits))
    axes[0, 0].set_ylim([0, 1100.])

    yunits = aisi304['elongation'].units
    axes[1, 0].set_xlabel('Neutron dose [{:s}]'.format(xunits))
    axes[1, 0].set_ylabel('Elongation [{:s}]'.format(yunits))
    axes[1, 0].set_ylim([0, 50.])
    axes[1, 0].legend()

    doses = np.array([1e20, 5e20, 1e21])
    temperature = np.linspace(300, 1000)
    yts = aisi304['strength_tensile_yield'].query_value(
            {'temperature': temperature}, 'thermal')
    elong = aisi304['elongation'].query_value(
            {'temperature': temperature}, 'thermal')
    axes[0, 1].plot(temperature, yts, label='unirradiated', color='black')
    axes[1, 1].plot(temperature, elong, label='unirradiated', color='black')

    colors = plt.cm.viridis(np.linspace(0, 0.75, len(doses)))
    for (dose, color) in zip(doses, colors):
        yts = aisi304['strength_tensile_yield'].query_value(
            {'temperature': temperature, 'neutron dose': dose}, 'radiation')
        elong = aisi304['elongation'].query_value(
            {'temperature': temperature, 'neutron dose': dose}, 'radiation')
        axes[0, 1].plot(temperature, yts, label='dose={:.1e} cm^-2'.format(dose), color=color)
        axes[1, 1].plot(temperature, elong, label='dose={:.1e} cm^-2'.format(dose), color=color)
    axes[0, 1].legend()
    xunits = aisi304['strength_tensile_yield']['radiation'].state_vars_units['temperature']
    axes[1, 1].set_xlabel('Temperature [{:s}]'.format(xunits))

    plt.suptitle('Effects of radiation on the strength and ductility of {:s}'.format(aisi304.name)
        + '\nin {:s} condition'.format(aisi304.condition))
    plt.tight_layout()
    plt.subplots_adjust(top=0.90, hspace=0.05, wspace=0.05)

    plt.show()

if __name__ == '__main__':
    main()
