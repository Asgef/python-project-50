import argparse

DESCRIPTION = 'Compares two configuration files and shows a difference.'


def get_pars_arg():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        help='set format of output',
        choices=['stylish', 'plain', 'json'],
        default='stylish'
    )
    args = parser.parse_args()

    return args
