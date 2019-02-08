"""Convert a property vs temperature table from WebPlotDigitizer csv to this project's YAML format."""

import argparse
import numpy as np

def main(args):
    data = np.genfromtxt(args.csv_filename, delimiter=',')
    temperature = data[:, 0]
    values = data[:, 1]
    print('temperature: ' + repr(temperature)[6:-1])
    print('values: ' + repr(values)[6:-1])


if __name__ == '__main__':
    #pylint: disable=invalid-name
    parser = argparse.ArgumentParser(
        description='Convert WebPlotDigitizer CSV to YAML')
    parser.add_argument("csv_filename", help='CSV file.')
    arguments = parser.parse_args()
    main(arguments)
