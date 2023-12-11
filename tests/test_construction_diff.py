from gendiff.construction_diff import add_node, create_diff


def test_add_node():
    node = add_node('key1', 'added', value_new='value2')
    assert node == {'key': 'key1', 'status': 'added', 'value_new': 'value2'}


def test_add_node_changed():
    node = add_node('key2', 'changed', value_old='value1', value_new='value2')
    assert node == {'key': 'key2', 'status': 'changed', 'value_old': 'value1', 'value_new': 'value2'}


def test_add_node_unchanged():
    node = add_node('key3', 'unchanged', value_old='value1', value_new='value2')
    assert node == {'key': 'key3', 'status': 'unchanged', 'value_old': 'value1', 'value_new': 'value2'}


def test_add_node_rm():
    node = add_node('key4', 'removed', value_old='value1')
    assert node == {'key': 'key4', 'status': 'removed', 'value_old': 'value1'}


def test_nested_node():
    children = [{'key': 'child1', 'status': 'removed', 'value_old': 'value_child'}]
    node = add_node('key5', 'nested', children=children)
    assert node == {"key": "key5", 'status': 'nested', 'children': children}


def test_create_diff():
    data1 = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': {'nested_key': 'nested_value'}
    }

    data2 = {
        'key1': 'value1',
        'key3': {'nested_key': 'modified_nested_value'},
        'key4': 'value4'
    }

    assert create_diff(data1, data2) == [
        {'key': 'key1', 'status': 'unchanged', 'value_old': 'value1'},
        {'key': 'key2', 'status': 'removed', 'value_old': 'value2'},
        {'key': 'key3', 'status': 'nested', 'children': [
            {'key': 'nested_key', 'status': 'changed', 'value_old': 'nested_value',
             'value_new': 'modified_nested_value'}]},
        {'key': 'key4', 'status': 'added', 'value_new': 'value4'}
    ]
