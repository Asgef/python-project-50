from gendiff.formatters.json_ import diff_json_format, get_json


def test_diff_json_format_added():
    data = [{'key': 'key1', 'status': 'added', 'value_new': 'value2'}]
    expected = {"key1": {"value": "value2", "status": "added"}}
    assert diff_json_format(data) == expected


def test_diff_json_format_changed():
    data = [{'key': 'key2', 'status': 'changed', 'value_old': 'value1', 'value_new': 'value2'}]
    expected = {"key2": {"value": "value1", "new value": "value2", "status": "changed"}}
    assert diff_json_format(data) == expected


def test_diff_json_format_rm():
    data = [{'key': 'key4', 'status': 'removed', 'value_old': 'value1'}]
    expected = {'key4': {"value": "value1", "status": "removed"}}
    assert diff_json_format(data) == expected


def test_diff_json_format_nested():
    data = [
        {'key': 'common', 'status': 'nested', 'children': [{'key': 'follow', 'status': 'added', 'value_new': 'false'}]}
    ]
    expected = {'common': {'value': {'follow': {'value': 'false', 'status': 'added'}}}}
    assert diff_json_format(data) == expected


def test_get_json():
    data = [{'key': 'key1', 'status': 'added', 'value_new': 'value2'}]
    expected = '{\n    "key1": {\n        "value": "value2",\n        "status": "added"\n    }\n}'
    assert get_json(data) == expected

