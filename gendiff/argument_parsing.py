import argparse

DESCRIPTION = 'Compares two configuration files and shows a difference.'


def get_pars_arg():
    """
    Parse command-line arguments for generating the difference report.

    This function sets up an ArgumentParser to handle command-line arguments.
    It defines the required positional arguments for the paths to the first
    and second files to compare. Additionally, it allows specifying an
    optional argument to choose the output format of the difference report.


    Parameters:
        - first_file: Path to the first file.
        - second_file: Path to the second file.
        - format: Format for output (default='stylish', 'plain', 'json').

    :return: Parsed input values (argparse arguments)
    """
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
