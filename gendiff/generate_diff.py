import json
import yaml
from gendiff.construction_diff import create_diff
from gendiff.formatters.stylish import diff_stylish_format
from gendiff.formatters.plain import diff_plain_format
from gendiff.formatters.json_ import get_json


def generate_diff(
        file_path1: str,
        file_path2: str,
        format:
        str = 'stylish'
) -> str:
    """
    Generate a difference report between two files.

    This function takes two file paths as input and compares the content of the
    files to generate a difference report. It loads the data from the files,
    finds the difference between the data, and then formats the difference
    using the specified output format (e.g., 'stylish', 'plain', 'json').

    :param file_path1: The path to the first file.
    :type file_path1: str
    :param file_path2:  The path to the second file.
    :type file_path2: str
    :param format: The output format for the difference report
                   (default is 'stylish').
    :type format: str
    :return: A string representation of the difference report.
    :rtype: str
    """
    file1 = open_file(file_path1)
    file2 = open_file(file_path2)

    diff = create_diff(file1, file2)

    return select_format(diff, format)


def select_format(data, form):
    """
    Sets the diff report output format based on the given argument

    :param data: Difference tree.
    :param form: Stylish, plain or json.
    :return: Formatted output.
    """
    if form == 'stylish':
        return diff_stylish_format(data)

    elif form == 'plain':
        return diff_plain_format(data)

    elif form == 'json':
        return get_json(data)


def open_file(file_path: str) -> dict:
    """
    Open and download the file in YAML or JSON format.

    This function takes a file path as arguments, opens the file,
    creates a file object and loads its contents as YAML or JSON data,
    depending on the file extension. The downloaded data is returned.

    :param file_path: Path to the file to open and load.
    :type file_path: str
    :return: Loaded data from file.
    :rtype: dict or list
    """
    with open(file_path, 'r') as file:

        if file_path.endswith('.json'):
            return json.load(file)

        else:

            return yaml.safe_load(file)
