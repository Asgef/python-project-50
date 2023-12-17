from gendiff.generate_diff import open_file
from gendiff.formatters.stylish import diff_stylish_format, format_node
from gendiff.construction_diff import create_diff
import os


def test_diff_stylish_format_added():
    data_added = [{'key': 'key1', 'status': 'added', 'value_new': 'value2'}]
    expected_added = '{\n  + key1: value2\n}'
    assert diff_stylish_format(data_added) == expected_added


def test_diff_stylish_format_changed():
    data_changed = [{'key': 'key2', 'status': 'changed', 'value_old': 'value1', 'value_new': 'value2'}]
    expected_changed = '{\n  - key2: value1\n  + key2: value2\n}'
    assert diff_stylish_format(data_changed) == expected_changed


def test_diff_stylish_format_unchanged():
    data_unchanged = [{'key': 'key3', 'status': 'unchanged', 'value_old': 'value1'}]
    expected_unchanged = '{\n    key3: value1\n}'
    assert diff_stylish_format(data_unchanged) == expected_unchanged


def test_diff_stylish_format_rm():
    data_rm = [{'key': 'key4', 'status': 'removed', 'value_old': 'value1'}]
    expected_rm = '{\n  - key4: value1\n}'
    assert diff_stylish_format(data_rm) == expected_rm


def test_diff_stylish_format_nested():
    data_nested = [
        {'key': 'common', 'status': 'nested', 'children': [{'key': 'follow', 'status': 'added', 'value_new': 'false'}]}]
    expected_nested = '{\n    common: {\n      + follow: false\n    }\n}'
    assert diff_stylish_format(data_nested) == expected_nested


def test_diff_format_general():
    test_directory = os.path.dirname(__file__)
    file_result = os.path.join(test_directory, 'fixtures/result_nested')
    with open(file_result, 'r') as expected_file:
        expected_data = expected_file.read()
        data = create_diff(
            open_file(os.path.join(test_directory, 'fixtures/file1_nested.json')),
            open_file(os.path.join(test_directory, 'fixtures/file2_nested.json'))
        )
        assert diff_stylish_format(data) == expected_data


def test_format_node():
    data_added = {'key': 'key1', 'status': 'added', 'value_new': '42'}
    expected_added = ['  + key1: 42']
    data_rm = {'key': 'key4', 'status': 'removed', 'value_old': 'null'}
    expected_rm = ['      - key4: null']
    data_changed = {'key': 'key2', 'status': 'changed', 'value_old': 'true', 'value_new': 'false'}
    expected_changed = ['  - key2: true', '  + key2: false']
    data_unchanged = {'key': 'key3', 'status': 'unchanged', 'value_old': 'value1'}
    expected_unchanged = ['    key3: value1']
    data_nested = {
        "key": "key5", 'status': 'nested',
        'children': [{
            'key': 'child1', 'status': 'removed', 'value_old': 'value_child'
        }]
    }
    expected_nested = ['       key5: {\n      - child1: value_child\n    }']

    assert format_node(data_added, 0, '    ') == expected_added
    assert format_node(data_rm, 1, '   ') == expected_rm
    assert format_node(data_changed, 0, '   ') == expected_changed
    assert format_node(data_unchanged, 0, '   ') == expected_unchanged
    assert format_node(data_nested, 0, '   ') == expected_nested
