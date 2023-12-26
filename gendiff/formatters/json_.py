import json


def get_json(data: list) -> str:
    """
    Create the difference tree in "json" format.

    This function takes the difference tree as input and converts
    it into a JSON-formatted string
    with indentation for better readability.

    :param data: The difference tree as a dictionary.
    :type data: dict
    :return: A string representation of the difference tree in "json" format.
    :rtype: str
    """
    return json.dumps(diff_json_format(data), indent=4)


def diff_json_format(data: list) -> str:
    """
    Recursively format the difference tree into a dictionary.

    This function iterates through the difference tree nodes and
    returns a string representation of the differences.
    Each node's key is associated with its type and relevant
    values like old_value, new_value, or nested differences.

    :param data: The difference node or subtree as a list of dictionaries.
    :type data: list
    :return: A string representation of the difference.
    :rtype: dict
    """
    diff_json = {}
    data.sort(key=lambda node: node['key'])

    for node in data:
        node_type = node['type']

        if node['type'] == 'added':
            diff_json[node['key']] = {
                'value': node['value_new'],
                'type': node_type
            }

        elif node['type'] in ['removed', 'unchanged']:
            diff_json[node['key']] = {
                'value': node['value_old'],
                'type': node_type
            }

        elif node['type'] == 'changed':
            diff_json[node['key']] = {
                'value': node['value_old'],
                'new value': node['value_new'],
                'type': node_type
            }

        elif node['type'] == 'nested':
            diff_json[node['key']] = {
                'value': diff_json_format(node['children'])
            }
        diff_json[node['key']]['type'] = node_type

    return diff_json
