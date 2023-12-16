import json


def get_json(data):
    return json.dumps(diff_json_format(data), indent=4)


def diff_json_format(data):
    diff_json = {}
    data.sort(key=lambda node: node['key'])

    for node in data:
        node_status = node['status']

        if node['status'] == 'added':
            diff_json[node['key']] = {
                'value': node['value_new'],
                'status': node_status
            }

        elif node['status'] in ['removed', 'unchanged']:
            diff_json[node['key']] = {
                'value': node['value_old'],
                'status': node_status
            }

        elif node['status'] == 'changed':
            diff_json[node['key']] = {
                'value': node['value_old'],
                'new value': node['value_new'],
                'status': node_status
            }

        elif node['status'] == 'nested':
            diff_json[node['key']] = {
                'value': diff_json_format(node['children'])
            }

    return diff_json
