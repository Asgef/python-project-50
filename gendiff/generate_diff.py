import json
import yaml
from gendiff.construction_diff import create_diff
from gendiff.formatters.stylish import diff_stylish_format
from gendiff.formatters.plain import diff_plain_format
from gendiff.formatters.json_ import get_json


def generate_diff(file_path1, file_path2, format='stylish'):
    file1 = open_file(file_path1)
    file2 = open_file(file_path2)

    diff = create_diff(file1, file2)

    return select_format(diff, format)


def select_format(data, form):
    if form == 'stylish':
        return diff_stylish_format(data)

    elif form == 'plain':
        return diff_plain_format(data)

    elif form == 'json':
        return get_json(data)


def open_file(file_path):
    with open(file_path, 'r') as file:

        if file_path.endswith('.json'):
            return json.load(file)

        else:

            return yaml.safe_load(file)
