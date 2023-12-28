def create_diff(data_1: dict, data_2: dict) -> list:
    """
    Compare the two dictionaries and get an idea of the differences.

    This function takes two dictionaries as input and compares their keys and
    meanings to identify differences between them. It returns a list,
    representing a tree where each node contains information about the key
    type (added, removed, unchanged, modified or nested) and
    corresponding values for the corresponding type.

    :param data_1: The first dictionary to compare.
    :type data_1: dict
    :param data_2: The second dictionary to compare.
    :type data_2: dict
    :return: A list representing the difference tree.
    :rtype: list
    """
    diff = []
    keys = sorted(data_1.keys() | data_2.keys())

    for key in keys:
        if key in data_1 and key not in data_2:
            node = {'key': key, 'type': 'removed', 'value_old': data_1[key]}

        elif key not in data_1 and key in data_2:
            node = {'key': key, 'type': 'added', 'value_new': data_2[key]}

        elif data_1[key] == data_2[key]:
            node = {
                'key': key, 'type': 'unchanged', 'value_old': data_1[key]
            }
        elif isinstance(data_1[key], dict) and isinstance(data_2[key], dict):
            child = create_diff(data_1[key], data_2[key])
            node = {'key': key, 'type': 'nested', 'children': child}

        else:
            node = {
                'key': key, 'type': 'changed',
                'value_old': data_1[key],
                'value_new': data_2[key]
            }

        diff.append(node)
    return diff
