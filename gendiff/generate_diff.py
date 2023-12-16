from gendiff.construction_diff import open_file, create_diff
from gendiff.formatters.stylish import diff_stylish_format
from gendiff.formatters.plain import diff_plain_format
from gendiff.formatters.json_ import get_json


def generate_diff(file1, file2, format='stylish'):
    file1 = open_file(file1)
    file2 = open_file(file2)

    diff = create_diff(file1, file2)

    return select_format(diff, format)


def select_format(data, form):
    if form == 'stylish':
        return diff_stylish_format(data)
    if form == 'plain':
        return diff_plain_format(data)
    if form == 'json':
        return get_json(data)
