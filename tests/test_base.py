from gendiff.base import generate_diff


def test_generate_diff():
    path1 = './tests/fixtures/file1.json'
    path2 = './tests/fixtures/file2.json'
    result = './tests/fixtures/result'
    with open(result) as result_file:
        assert generate_diff(path1, path2) == result_file.read()
