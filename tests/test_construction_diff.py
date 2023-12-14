from gendiff.construction_diff import add_node, create_diff, format_value, open_file
import os


def test_add_node():
    node = add_node('key1', 'added', value_new='value2')
    assert node == {'key': 'key1', 'status': 'added', 'value_new': 'value2'}


def test_add_node_changed():
    node = add_node('key2', 'changed', value_old='value1', value_new='value2')
    assert node == {'key': 'key2', 'status': 'changed', 'value_old': 'value1', 'value_new': 'value2'}


def test_add_node_unchanged():
    node = add_node('key3', 'unchanged', value_old='value1')
    assert node == {'key': 'key3', 'status': 'unchanged', 'value_old': 'value1'}


def test_add_node_rm():
    node = add_node('key4', 'removed', value_old='value1')
    assert node == {'key': 'key4', 'status': 'removed', 'value_old': 'value1'}


def test_nested_node():
    children = [{'key': 'child1', 'status': 'removed', 'value_old': 'value_child'}]
    node = add_node('key5', 'nested', children=children)
    assert node == {"key": "key5", 'status': 'nested', 'children': children}


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
        {'key': 'key3', 'status': 'nested', 'children': [
            {'key': 'nested_key', 'status': 'changed', 'value_old': 'nested_value',
             'value_new': 'modified_nested_value'}]},
        {'key': 'key4', 'status': 'added', 'value_new': 'true'}
    ]


def test_format_value():
    assert format_value(True) == 'true'
    assert format_value(False) == 'false'
    assert format_value(None) == 'null'
    assert format_value(42) == '42'
    assert format_value([42]) == '[42]'
    assert format_value({'value': {'val1': True}}) == {'value': {'val1': 'true'}}


def test_open_file():
    test_directory = os.path.dirname(__file__)
    expected = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False
    }
    assert open_file(os.path.join(test_directory, 'fixtures/file1.json')) == expected
    assert open_file(os.path.join(test_directory, 'fixtures/file1.yml')) == expected
