from gendiff.generate_diff import open_file
from gendiff.construction_diff import create_diff
from gendiff.formatters.plain import diff_plain_format
import os


def test_diff_plain_format_added():
    data = [{'key': 'key1', 'status': 'added', 'value_new': 2}]
    expected = "Property 'key1' was added with value: 2"
    assert diff_plain_format(data) == expected


def test_diff_plain_format_changed():
    data = [{'key': 'key2', 'status': 'changed', 'value_old': 'value1', 'value_new': 'value2'}]
    expected = "Property 'key2' was updated. From 'value1' to 'value2'"
    assert diff_plain_format(data) == expected


def test_diff_plain_format_rm():
    data = [{'key': 'key4', 'status': 'removed', 'value_old': 'value1'}]
    expected = "Property 'key4' was removed"
    assert diff_plain_format(data) == expected


def test_diff_plain_format_nested():
    data = [
        {'key': 'common', 'status': 'nested', 'children': [{'key': 'follow', 'status': 'added', 'value_new': 'false'}]}
    ]
    expected = "Property 'common.follow' was added with value: false"
    assert diff_plain_format(data) == expected


def test_diff_plain_format_complex():
    data = [{'key': 'key1', 'status': 'added', 'value_new': {'key': 'follow'}}]
    expected = "Property 'key1' was added with value: [complex value]"
    assert diff_plain_format(data) == expected


def test_plain_general():
    test_directory = os.path.dirname(__file__)
    file_result = os.path.join(test_directory, 'fixtures/results/result_plain')
    with open(file_result, 'r') as expected_file:
        expected = expected_file.read()
        data = create_diff(
            open_file(os.path.join(test_directory, 'fixtures/file1_nested.json')),
            open_file(os.path.join(test_directory, 'fixtures/file2_nested.json'))
        )
        assert diff_plain_format(data) == expected
