import pytest
from gendiff.formatters.stylish import diff_stylish_format, format_node
from gendiff.formatters.plain import diff_plain_format
from gendiff.formatters.json_ import diff_json_format


test_data = {
    'added': [{
        'key': 'key1',
        'type': 'added',
        'value_new': 2
    }],
    'changed': [{
        'key': 'key2',
        'type': 'changed',
        'value_old': 'value1',
        'value_new': 'value2'
    }],
    'removed': [{
        'key': 'key4',
        'type': 'removed',
        'value_old': 'value1'
    }],
    'nested': [{
        'key': 'common', 'type': 'nested', 'children': [{
            'key': 'follow',
            'type': 'added',
            'value_new': 'false'
        }]
    }],
    'complex': [{
        'key': 'key1',
        'type': 'added',
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
        {"key1": {"value": 2, "type": "added"}}
    ),
    (
        diff_json_format, test_data['changed'],
        {"key2": {
            "value": "value1", "new value": "value2", "type": "changed"
        }}
    ),
    (
        diff_json_format, test_data['removed'],
        {'key4': {"value": "value1", "type": "removed"}}
    ),
    (
        diff_json_format, test_data['nested'],
        {
            'common': {
                'type': 'nested',
                'value': {'follow': {'type': 'added', 'value': 'false'}}
            }
        }
    ),
]


@pytest.mark.parametrize("format_function, data, expected", test_cases)
def test_formatting(format_function, data, expected):
    assert format_function(data) == expected


test_data = {
    'added': {
        'key': 'key1',
        'type': 'added',
        'value_new': 42
    },
    'removed': {
        'key': 'key4',
        'type': 'removed',
        'value_old': 'null'
    },
    'changed': {
        'key': 'key2',
        'type': 'changed',
        'value_old': 'true',
        'value_new': 'false'
    },
    'unchanged': {
        'key': 'key3',
        'type': 'unchanged',
        'value_old': 'value1'
    },
    'nested': {
        "key": "key5",
        'type': 'nested',
        'children': [{
            'key': 'child',
            'type': 'removed',
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
