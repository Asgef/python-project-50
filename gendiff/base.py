import json


def generate_diff(path_file1, path_file2):
    file1 = json.load(open(path_file1))
    file2 = json.load(open(path_file2))
    data = select_data(file1, file2)
    analyze = analyze_data(data)
    return analyze


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
                res_diff.append(f'    {key}: {data[key]['first_file']}')
            else:
                res_diff.append(f'  - {key}: {data[key]['first_file']}')
                res_diff.append(f'  + {key}: {data[key]['second_file']}')
        if 'first_file' in data[key] and 'second_file' not in data[key]:
            res_diff.append(f'  - {key}: {data[key]['first_file']}')
        if 'first_file' not in data[key] and 'second_file' in data[key]:
            res_diff.append(f'  + {key}: {data[key]['second_file']}')
    return '{\n' + '\n'.join(res_diff) + '\n}'
