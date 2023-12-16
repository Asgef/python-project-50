from gendiff.formatters.json_ import diff_json_format


def test_diff_json_format_added():
    data = [{'key': 'key1', 'status': 'added', 'value_new': 'value2'}]
    expected = {'key1': 'value2'}
    assert diff_json_format(data) == expected


def test_diff_json_format_changed():
    data = [{'key': 'key2', 'status': 'changed', 'value_old': 'value1', 'value_new': 'value2'}]
    expected = {'key2': {'value': 'value1', 'new value': 'value2'}}
    assert diff_json_format(data) == expected


def test_diff_json_format_rm():
    data = [{'key': 'key4', 'status': 'removed', 'value_old': 'value1'}]
    expected = {'key4': 'value1'}
    assert diff_json_format(data) == expected


def test_diff_json_format_nested():
    data = [
        {'key': 'common', 'status': 'nested', 'children': [{'key': 'follow', 'status': 'added', 'value_new': 'false'}]}
    ]
    expected = {'common': {'follow': 'false'}}
    assert diff_json_format(data) == expected

