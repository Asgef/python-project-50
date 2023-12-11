from gendiff.generate_diff import generate_diff, open_file


def test_open_file():
    expected = {
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": False
    }
    assert open_file('fixtures/file1.json') == expected
    assert open_file('fixtures/file1.yml') == expected


def test_generate_diff_json():
    with (
        open('fixtures/result', 'r') as result,
        open('fixtures/file1.json', 'r') as file1,
        open('fixtures/file2.json', 'r') as file2
    ):
        assert generate_diff(file1, file2) == result


def test_generate_diff_yml():
    with (
        open('fixtures/result', 'r') as result,
        open('fixtures/file1.yml', 'r') as file1,
        open('fixtures/file2.yml', 'r') as file2
    ):
        assert generate_diff(file1, file2) == result
