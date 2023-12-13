from gendiff.stylish import diff_format, format_node


def test_diff_format_added():
    data_added = [{'key': 'key1', 'status': 'added', 'value_new': 'value2'}]
    expected_added = '{\n  + key1: value2\n}'
    assert diff_format(data_added) == expected_added


def test_diff_format_changed():
    data_changed = [{'key': 'key2', 'status': 'changed', 'value_old': 'value1', 'value_new': 'value2'}]
    expected_changed = '{\n  - key2: value1\n  + key2: value2\n}'
    assert diff_format(data_changed) == expected_changed


def test_diff_format_unchanged():
    data_unchanged = [{'key': 'key3', 'status': 'unchanged', 'value_old': 'value1'}]
    expected_unchanged = '{\n    key3: value1\n}'
    assert diff_format(data_unchanged) == expected_unchanged


def test_diff_format_rm():
    data_rm = [{'key': 'key4', 'status': 'removed', 'value_old': 'value1'}]
    expected_rm = '{\n  - key4: value1\n}'
    assert diff_format(data_rm) == expected_rm


def test_diff_format_nested():
    data_nested = [{
        "key": "key5", 'status': 'nested',
        'children': {
            'key': 'child1', 'status': 'removed', 'value_old': 'value_child'
        }
    }]
    expected_nested = '{\n    key5: {\n      - child1: value_child\n    }\n}'
    assert diff_format(data_nested) == expected_nested


def test_format_node():
    data_added = {'key': 'key1', 'status': 'added', 'value_new': '42'}
    expected_added = '\n  + key1: 42'
    data_rm = {'key': 'key4', 'status': 'removed', 'value_old': 'null'}
    expected_rm = '\n      - key4: null'
    data_changed = {'key': 'key2', 'status': 'changed', 'value_old': 'true', 'value_new': 'false'}
    expected_changed = '\n  - key2: true\n  + key2: false'
    data_unchanged = {'key': 'key3', 'status': 'unchanged', 'value_old': 'value1'}
    expected_unchanged = '\n    key3: value1'
    data_nested = {
        "key": "key5", 'status': 'nested',
        'children': {
            'key': 'child1', 'status': 'removed', 'value_old': 'value_child'
        }
    }
    expected_nested = '\n    key5: {\n      - child1: value_child\n    }'

    assert format_node(data_added, 0, 4, ' ') == expected_added
    assert format_node(data_rm, 1, 4, ' ') == expected_rm
    assert format_node(data_changed, 0, 4, ' ') == expected_changed
    assert format_node(data_unchanged, 0, 4, ' ') == expected_unchanged
    assert format_node(data_nested, 0, 4, ' ') == expected_nested
