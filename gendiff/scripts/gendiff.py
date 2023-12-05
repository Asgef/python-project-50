#!/usr/bin/env python3

import argparse


DESCRIPTION = 'Compares two configuration files and shows a difference.'


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    parser.parse_args()


if __name__ == '__main__':
    main()
