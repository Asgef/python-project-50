import json
import yaml
from construction_diff import create_diff


# def generate_diff(file1, file2):
#     file1 = open_file(file1)
#     file2 = open_file(file2)
#
#     data = create_diff(file1, file2)
#     analyze = _(data)
#     return analyze


def open_file(file_path):
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        else:
            return yaml.safe_load(file)



#
#
# def create_data(sing, name, value):
#     if isinstance(value, bool):
#         if value:
#             value = 'true'
#         else:
#             value = 'false'
#     return f'  {sing} {name}: {value}'
