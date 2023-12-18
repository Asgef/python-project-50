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
