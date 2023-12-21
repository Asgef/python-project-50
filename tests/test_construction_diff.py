import pytest

from gendiff.generate_diff import open_file
from gendiff.construction_diff import add_node, create_diff, format_value
import os


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


def test_open_file():
    test_directory = os.path.dirname(__file__)
    expected = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False
    }

    assert open_file(
        os.path.join(test_directory, 'fixtures/file1.json')
    ) == expected

    assert open_file(
        os.path.join(test_directory, 'fixtures/file1.yml')
    ) == expected
