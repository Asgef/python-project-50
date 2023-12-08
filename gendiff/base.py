import json
import yaml


def generate_diff(file1, file2):
    file1 = open_file(file1)
    file2 = open_file(file2)

    data = select_data(file1, file2)
    analyze = analyze_data(data)
    return analyze


def open_file(file_path):
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        else:
            return yaml.safe_load(file)


def select_data(file1, file2):
    data = {'names': []}
    for key in file1:
        data[key] = {'first_file': file1[key]}
        data['names'].append(key)

    for key in file2:
        if key in data:
            data[key]['second_file'] = file2[key]
        else:
            data[key] = {'second_file': file2[key]}
            data['names'].append(key)
    return data


def analyze_data(data):
    res_diff = []
    data['names'].sort()
    for key in data['names']:
        if 'first_file' in data[key] and 'second_file' in data[key]:
            if data[key]['first_file'] == data[key]['second_file']:
                res_diff.append(create_data(' ', key, data[key]['first_file']))
            else:
                res_diff.append(create_data('-', key, data[key]['first_file']))
                res_diff.append(create_data('+', key, data[key]['second_file']))
        if 'first_file' in data[key] and 'second_file' not in data[key]:
            res_diff.append(create_data('-', key, data[key]['first_file']))
        if 'first_file' not in data[key] and 'second_file' in data[key]:
            res_diff.append(create_data('+', key, data[key]['second_file']))
    return '{\n' + '\n'.join(res_diff) + '\n}'


def create_data(sing, name, value):
    if isinstance(value, bool):
        if value:
            value = 'true'
        else:
            value = 'false'
    return f'  {sing} {name}: {value}'
