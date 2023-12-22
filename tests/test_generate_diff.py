import os
import pytest
from gendiff.generate_diff import generate_diff


def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()


test_directory = os.path.dirname(__file__)
file1 = os.path.join(test_directory, 'fixtures/file1_nested.json')
file2 = os.path.join(test_directory, 'fixtures/file2_nested.json')
plain_res = os.path.join(test_directory, 'fixtures/results/plain_nested')
stylish_res = os.path.join(test_directory, 'fixtures/results/stylish_nested')
json_res = os.path.join(test_directory, 'fixtures/results/json_nested')

test_cases = [
    (generate_diff, file1, file2, 'stylish', stylish_res),
    (generate_diff, file1, file2, 'plain', plain_res),
    (generate_diff, file1, file2, 'json', json_res)
]


@pytest.mark.parametrize(
    "generate_diff_func, file1, file2, format_, expected_file", test_cases
)
def test_diff_format(generate_diff_func, file1, file2, format_, expected_file):
    expected = read_file(expected_file)
    actual = generate_diff_func(str(file1), str(file2), format_)
    assert actual == expected
