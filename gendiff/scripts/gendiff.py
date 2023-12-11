#!/usr/bin/env python3

from gendiff.construction_diff import generate_diff
from gendiff.argument_parsing import get_pars_arg


def main():
    argument = get_pars_arg()
    diff = generate_diff(argument.first_file, argument.second_file)
    print(diff)


if __name__ == '__main__':
    main()
