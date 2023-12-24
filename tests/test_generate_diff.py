import os
import pytest
from gendiff.parser import parse
from gendiff.generate_diff import generate_diff
from gendiff.construction_diff import add_node, create_diff, format_value


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


@pytest.mark.parametrize(
    "key, status, value_old, value_new, children, expected",
    [
        (
            'key1', 'added', None, 'value2', None, {
                'key': 'key1',
                'status': 'added',
                'value_new': 'value2'
            }
        ),
        (
            'key2', 'changed', 'value1', 'value2', None, {
                'key': 'key2',
                'status': 'changed',
                'value_old': 'value1',
                'value_new': 'value2'
            }
        ),
        (
            'key3', 'unchanged', 'value1', None, None, {
                'key': 'key3',
                'status': 'unchanged',
                'value_old': 'value1'
            }
        ),
        (
            'key4', 'removed', 'value1', None, None, {
                'key': 'key4',
                'status': 'removed',
                'value_old': 'value1'
            }
        ),
        (
            'key5', 'nested', None, None, [{
                'key': 'child1',
                'status': 'removed',
                'value_old': 'value_child'
            }],
            {
                "key": "key5", 'status': 'nested', 'children': [{
                    'key': 'child1',
                    'status': 'removed',
                    'value_old': 'value_child'
                }]
            }
        )
    ]
)
def test_add_node(key, status, value_old, value_new, children, expected):
    if children is None:
        node = add_node(key, status, value_old=value_old, value_new=value_new)
    else:
        node = add_node(key, status, children=children)
    assert node == expected


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
        {'key': 'key1', 'status': 'unchanged', 'value_old': 'null'},
        {'key': 'key2', 'status': 'removed', 'value_old': 'value2'},
        {
            'key': 'key3', 'status': 'nested', 'children': [{
                'key': 'nested_key',
                'status': 'changed',
                'value_old': 'nested_value',
                'value_new': 'modified_nested_value'
            }]
        },
        {'key': 'key4', 'status': 'added', 'value_new': 'true'}
    ]


@pytest.mark.parametrize("data, expected", [
    (True, 'true'),
    (False, 'false'),
    (None, 'null'),
    (42, 42),
    ([42], '[42]'),
    ({'value': {'val1': True}}, {'value': {'val1': 'true'}})
])
def test_format_value(data, expected):
    assert format_value(data) == expected
