"""Convert a property vs temperature table from WebPlotDigitizer csv to this project's YAML format."""
import os.path
import argparse
import yaml
import numpy as np


# See https://stackoverflow.com/a/33944926
def float_representer(dumper, value):
    if abs(value) < 1e6:
        text = '{0:.4f}'.format(value)
    else:
        text = '{:.4e}'.format(value)
    return dumper.represent_scalar(u'tag:yaml.org,2002:float', text)
yaml.add_representer(float, float_representer)


def make_yaml_dict(filename, args):
    data = np.genfromtxt(filename, delimiter=',')
    temperature = data[:, 0]
    if args.fahrenheit:
        # Convert to kelvin.
        temperature = (temperature - 32.) * (5./9) + 273.15
    values = data[:, 1]
    values = values * args.yscale
    yaml_dict = {
        'temperature': [float(x) for x in temperature],
        'values': [float(x) for x in values],
    }
    return yaml_dict


def main(args):
    if os.path.isdir(args.in_filename):
        yaml_dict = {}
        for file in os.listdir(args.in_filename):
            print(file)
            if os.path.splitext(file)[1] == '.csv':
                name = file[:-4]
                yaml_dict[name] = make_yaml_dict(os.path.join(args.in_filename, file), args)
    else:
        yaml_dict = make_yaml_dict(args.in_filename, args)
    yaml_doc = yaml.dump(yaml_dict)
    print(yaml_doc)
    with open('out.yaml', 'w') as outfile:
        outfile.write(yaml_doc)


if __name__ == '__main__':
    #pylint: disable=invalid-name
    parser = argparse.ArgumentParser(
        description='Convert WebPlotDigitizer CSV to YAML')
    parser.add_argument('in_filename', help='CSV file or directory of csv files.')
    parser.add_argument('-f', '--fahrenheit', help='Use flag if temperature in csv is in Fahrenheit, will be converted to kelvin', action='store_true')
    parser.add_argument('--yscale', help='Scaling factor for y-axis data', type=float, default=1.0)
    arguments = parser.parse_args()
    main(arguments)
