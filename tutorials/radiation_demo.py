import os.path
import numpy as np
import matplotlib.pyplot as plt
import materials

def main():
    filename = os.path.join(materials.get_database_dir(), 'AISI_304.yaml')
    aisi304 = materials.load_from_yaml(filename, 'sheet and strip', 'annealed')
    dose = np.logspace(19.5, 22)
    temperatures = np.array([300, 300+273, 600+273, 700+273, 1023])
    colors = plt.cm.hot(np.linspace(0, 0.5, len(temperatures)))
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex='col')
    for (temp, color) in zip(temperatures, colors):
        temp_array = np.full_like(dose, temp)
        yts = aisi304['strength_tensile_yield'].query_value(
            {'temperature': temp_array, 'neutron dose': dose}, 'radiation')
        elong = aisi304['elongation'].query_value(
            {'temperature': temp_array, 'neutron dose': dose}, 'radiation')
        axes[0].semilogx(dose, yts, label='$T={:.0f}$ K'.format(temp), color=color)
        axes[1].semilogx(dose, elong, label='$T={:.0f}$ K'.format(temp), color=color)
    xunits = aisi304['strength_tensile_yield']['radiation'].state_vars_units['neutron dose']
    yunits = aisi304['strength_tensile_yield'].units
    axes[0].set_ylabel('Yield tensile strength [{:s}]'.format(yunits))
    axes[0].set_ylim([0, 1100.])
    axes[0].set_title('Effects of radiation on the strength and ductility of {:s}'.format(aisi304.name))
    axes[0].legend()

    yunits = aisi304['elongation'].units
    axes[1].set_xlabel('Neutron dose [{:s}]'.format(xunits))
    axes[1].set_ylabel('Elongation [{:s}]'.format(yunits))
    axes[1].set_ylim([0, 50.])
    axes[1].legend()

    plt.subplots_adjust(hspace=0.05)

    plt.show()

if __name__ == '__main__':
    main()
