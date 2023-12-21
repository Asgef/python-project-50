import os
import pytest
from gendiff.formatters.stylish import diff_stylish_format, format_node
from gendiff.formatters.plain import diff_plain_format
from gendiff.formatters.json_ import get_json, diff_json_format
from gendiff.construction_diff import create_diff
from gendiff.generate_diff import open_file

test_data = {
    'added': [{
        'key': 'key1',
        'status': 'added',
        'value_new': 2
    }],
    'changed': [{
        'key': 'key2',
        'status': 'changed',
        'value_old': 'value1',
        'value_new': 'value2'
    }],
    'removed': [{
        'key': 'key4',
        'status': 'removed',
        'value_old': 'value1'
    }],
    'nested': [{
        'key': 'common', 'status': 'nested', 'children': [{
            'key': 'follow',
            'status': 'added',
            'value_new': 'false'
        }]
    }],
    'complex': [{
        'key': 'key1',
        'status': 'added',
        'value_new': {'key': 'follow'}
    }],
}

test_cases = [
    (
        diff_stylish_format, test_data['added'],
        '{\n  + key1: 2\n}'
    ),
    (
        diff_stylish_format, test_data['changed'],
        '{\n  - key2: value1\n  + key2: value2\n}'
    ),
    (
        diff_stylish_format, test_data['removed'],
        '{\n  - key4: value1\n}'
    ),
    (
        diff_stylish_format, test_data['nested'],
        '{\n    common: {\n      + follow: false\n    }\n}'
    ),

    (
        diff_plain_format, test_data['added'],
        "Property 'key1' was added with value: 2"
    ),
    (
        diff_plain_format, test_data['changed'],
        "Property 'key2' was updated. From 'value1' to 'value2'"
    ),
    (
        diff_plain_format, test_data['removed'],
        "Property 'key4' was removed"),
    (
        diff_plain_format, test_data['nested'],
        "Property 'common.follow' was added with value: false"
    ),
    (
        diff_plain_format, test_data['complex'],
        "Property 'key1' was added with value: [complex value]"
    ),

    (
        diff_json_format, test_data['added'],
        {"key1": {"value": 2, "status": "added"}}
    ),
    (
        diff_json_format, test_data['changed'],
        {"key2": {
            "value": "value1", "new value": "value2", "status": "changed"
        }}
    ),
    (
        diff_json_format, test_data['removed'],
        {'key4': {"value": "value1", "status": "removed"}}
    ),
    (
        diff_json_format, test_data['nested'],
        {'common': {
            'value': {'follow': {'value': 'false', 'status': 'added'}}
        }}
    ),
]


@pytest.mark.parametrize("format_function, data, expected", test_cases)
def test_formatting(format_function, data, expected):
    assert format_function(data) == expected


def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()


test_directory = os.path.dirname(__file__)
file1_nested = os.path.join(test_directory, 'fixtures/file1_nested.json')
file2_nested = os.path.join(test_directory, 'fixtures/file2_nested.json')
result_plain = os.path.join(test_directory, 'fixtures/results/result_plain')
result_nested = os.path.join(test_directory, 'fixtures/results/result_nested')

test_cases = [
    (diff_plain_format, file1_nested, file2_nested, result_plain),
    (diff_stylish_format, file1_nested, file2_nested, result_nested),
]


@pytest.mark.parametrize(
    "format_function, file1, file2, expected_file", test_cases
)
def test_diff_format(format_function, file1, file2, expected_file):
    expected = read_file(expected_file)
    data = create_diff(open_file(file1), open_file(file2))
    assert format_function(data) == expected


def test_get_json():
    data = [{'key': 'key1', 'status': 'added', 'value_new': 'value2'}]
    expected = (
        '{\n'
        '    "key1": {\n'
        '        "value": "value2",\n'
        '        "status": "added"\n'
        '    }\n'
        '}'
    )
    assert get_json(data) == expected


test_data = {
    'added': {
        'key': 'key1',
        'status': 'added',
        'value_new': 42
    },
    'removed': {
        'key': 'key4',
        'status': 'removed',
        'value_old': 'null'
    },
    'changed': {
        'key': 'key2',
        'status': 'changed',
        'value_old': 'true',
        'value_new': 'false'
    },
    'unchanged': {
        'key': 'key3',
        'status': 'unchanged',
        'value_old': 'value1'
    },
    'nested': {
        "key": "key5",
        'status': 'nested',
        'children': [{
            'key': 'child',
            'status': 'removed',
            'value_old': 'value_child'
        }]
    },
}

test_cases = [
    (
        format_node, test_data['added'], 0, '    ',
        ['  + key1: 42']
    ),
    (
        format_node, test_data['removed'], 1, '   ',
        ['      - key4: null']
    ),
    (
        format_node, test_data['changed'], 0, '   ',
        ['  - key2: true', '  + key2: false']
    ),
    (
        format_node, test_data['unchanged'], 0, '   ',
        ['    key3: value1']
    ),
    (
        format_node, test_data['nested'], 0, '   ',
        ['       key5: {\n      - child: value_child\n    }']
    ),
]


@pytest.mark.parametrize(
    "format_function, data, depth, indent, expected", test_cases
)
def test_format_node(format_function, data, depth, indent, expected):
    assert format_function(data, depth, indent) == expected
