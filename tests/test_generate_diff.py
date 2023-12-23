import os
import pytest
from gendiff.generate_diff import generate_diff, open_file
from gendiff.parser import parse


def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()


test_directory = os.path.dirname(__file__)
file1 = os.path.join(test_directory, 'fixtures/file1_nested.json')
file2 = os.path.join(test_directory, 'fixtures/file2_nested.json')
plain_res = os.path.join(test_directory, 'fixtures/results/plain_nested')
stylish_res = os.path.join(test_directory, 'fixtures/results/stylish_nested')
json_res = os.path.join(test_directory, 'fixtures/results/json_nested')

test_cases = [
    (generate_diff, file1, file2, 'stylish', stylish_res),
    (generate_diff, file1, file2, 'plain', plain_res),
    (generate_diff, file1, file2, 'json', json_res)
]


@pytest.mark.parametrize(
    "generate_diff_func, file1, file2, format_, expected_file", test_cases
)
def test_diff_format(generate_diff_func, file1, file2, format_, expected_file):
    expected = read_file(expected_file)
    actual = generate_diff_func(str(file1), str(file2), format_)
    assert actual == expected


def test_open_file():
    data_json = os.path.join(test_directory, 'fixtures/file1.json')
    data_yaml = os.path.join(test_directory, 'fixtures/file1.yml')

    expected_json = (
        '{\n'
        '  "host": "hexlet.io",\n'
        '  "timeout": 50,\n'
        '  "proxy": "123.234.53.22",\n'
        '  "follow": false\n'
        '}\n',
        'json'
    )
    expected_yaml = (
        'host: "hexlet.io"\n'
        'timeout: 50\n'
        'proxy: "123.234.53.22"\n'
        'follow: false',
        'yaml'
    )

    assert open_file(data_json) == expected_json
    assert open_file(data_yaml) == expected_yaml
    invalid_file = os.path.join(test_directory, 'fixtures/invalid.txt')
    with pytest.raises(FileNotFoundError) as excinfo:
        open_file(invalid_file)
    assert 'invalid file format' in str(excinfo.value)


def test_parse():
    data_json = (
        '{\n'
        '  "host": "hexlet.io",\n'
        '  "timeout": 50,\n'
        '  "proxy": "123.234.53.22",\n'
        '  "follow": false\n'
        '}\n'
    )
    data_yml = (
        'host: "hexlet.io"\n'
        'timeout: 50\n'
        'proxy: "123.234.53.22"\n'
        'follow: false'
    )
    expected = {
        'host': 'hexlet.io',
        'timeout': 50,
        'proxy': '123.234.53.22',
        'follow': False
    }
    assert parse(data_json, 'json') == expected
    assert parse(data_yml, 'yaml') == expected
    with pytest.raises(FileNotFoundError) as excinfo:
        parse(data_yml, 'txt')
    assert 'Invalid data_format: txt' in str(excinfo.value)
