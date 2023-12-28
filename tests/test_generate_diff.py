import os
import pytest
from gendiff.parser import parse
from gendiff.generate_diff import generate_diff
from gendiff.construction_diff import create_diff


def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()


test_directory = os.path.dirname(__file__)
file1_json = os.path.join(test_directory, 'fixtures/file1_nested.json')
file2_json = os.path.join(test_directory, 'fixtures/file2_nested.json')
file1_yaml = os.path.join(test_directory, 'fixtures/file1_nested.yaml')
file2_yaml = os.path.join(test_directory, 'fixtures/file2_nested.yaml')
plain_res = os.path.join(test_directory, 'fixtures/results/plain_nested')
stylish_res = os.path.join(test_directory, 'fixtures/results/stylish_nested')
json_res = os.path.join(test_directory, 'fixtures/results/json_nested')

test_cases = [
    (generate_diff, file1_json, file2_json, 'stylish', stylish_res),
    (generate_diff, file1_json, file2_json, 'plain', plain_res),
    (generate_diff, file1_json, file2_json, 'json', json_res),
    (generate_diff, file1_yaml, file2_yaml, 'stylish', stylish_res),
    (generate_diff, file1_yaml, file2_yaml, 'plain', plain_res),
    (generate_diff, file1_yaml, file2_yaml, 'json', json_res)

]


@pytest.mark.parametrize(
    "generate_diff_func, file1, file2, format_, expected_file", test_cases
)
def test_generate_diff(
        generate_diff_func,
        file1,
        file2,
        format_,
        expected_file
):
    expected = read_file(expected_file)
    actual = generate_diff_func(str(file1), str(file2), format_)
    assert actual == expected


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


@pytest.mark.parametrize("data, data_format, expected", [
    (data_json, 'json', expected),
    (data_yml, 'yaml', expected),
])
def test_parse(data, data_format, expected):
    assert parse(data, data_format) == expected


def test_create_diff():
    data1 = {
        'key1': None,
        'key2': 'value2',
        'key3': {'nested_key': 'nested_value'}
    }

    data2 = {
        'key1': None,
        'key3': {'nested_key': 'modified_nested_value'},
        'key4': True
    }

    assert create_diff(data1, data2) == [
        {'key': 'key1', 'type': 'unchanged', 'value_old': None},
        {'key': 'key2', 'type': 'removed', 'value_old': 'value2'},
        {
            'key': 'key3', 'type': 'nested', 'children': [{
                'key': 'nested_key',
                'type': 'changed',
                'value_old': 'nested_value',
                'value_new': 'modified_nested_value'
            }]
        },
        {'key': 'key4', 'type': 'added', 'value_new': True}
    ]
