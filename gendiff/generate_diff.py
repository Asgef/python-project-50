from gendiff.construction_diff import create_diff
from gendiff.formatters.stylish import diff_stylish_format
from gendiff.formatters.plain import diff_plain_format
from gendiff.formatters.json_ import get_json
from gendiff.parser import parse


def generate_diff(
        path1: str,
        path2: str,
        format:
        str = 'stylish'
) -> str:
    """
    Generate a difference report between two files.

    This function takes two file paths as input and compares the content of the
    files to generate a difference report. It loads the data from the files,
    finds the difference between the data, and then formats the difference
    using the specified output format (e.g., 'stylish', 'plain', 'json').

    :param path1: The path to the first file.
    :type path1: str
    :param path2:  The path to the second file.
    :type path2: str
    :param format: The output format for the difference report
                   (default is 'stylish').
    :type format: str
    :return: A string representation of the difference report.
    :rtype: str
    """
    data1 = parse(*open_file(path1))
    data2 = parse(*open_file(path2))

    diff = create_diff(data1, data2)

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


def open_file(file_path: str) -> tuple[str, str]:
    """
    Open and download the file in YAML or JSON format.

    This function takes a file path as arguments,
    opens the file in YAML or JSON format, creates a file object,
    and converts the data to a string.
    The loaded data is returned as a tuple, text data
    and a string with the name of the extension.

    :param file_path: Path to the file to open and load.
    :type file_path: str
    :return: Loaded data and format.
    :rtype: tuple
    """
    with open(file_path, 'r') as file:
        text = file.read()
    if file_path.endswith('.json'):
        data_format = 'json'
    elif file_path.endswith('yaml') or file_path.endswith('yml'):
        data_format = 'yaml'

    return text, data_format
