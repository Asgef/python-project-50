def create_diff(file1: dict, file2: dict) -> list:
    """
    Compare the two dictionaries and get an idea of the differences.

    This function takes two dictionaries as input and compares their keys and
    meanings to identify differences between them. It returns a list,
    representing a tree where each node contains information about the key
    type (added, removed, unchanged, modified or nested) and
    corresponding values for the corresponding type.

    :param file1: The first dictionary to compare.
    :type file1: dict
    :param file2: The second dictionary to compare.
    :type file2: dict
    :return: A list representing the difference tree.
    :rtype: list
    """
    diff = []
    keys = sorted(file1.keys() | file2.keys())

    for key in keys:
        if key in file1 and key not in file2:
            node = add_node(key, 'removed', value_old=format_value(file1[key]))

        elif key not in file1 and key in file2:
            node = add_node(key, 'added', value_new=format_value(file2[key]))

        elif file1[key] == file2[key]:
            node = add_node(
                key, 'unchanged', value_old=format_value(file1[key])
            )
        elif isinstance(file1[key], dict) and isinstance(file2[key], dict):
            child = create_diff(file1[key], file2[key])
            node = add_node(key, 'nested', children=child)

        else:
            node = add_node(
                key, 'changed',
                value_old=format_value(file1[key]),
                value_new=format_value(file2[key])
            )

        diff.append(node)
    return diff


def add_node(
        key: str,
        type: str,
        value_old=None,
        value_new=None,
        children=None
) -> dict:
    """
    Create a diff tree node.

    This function creates a node for the diff tree representing
    the difference between two keys in the compared dictionaries. Knot
    contains information about the key, difference type (added,
    deleted, modified, not modified, or nested), as well as the corresponding
    values for corresponding difference type.

    :param key: The key representing the difference.
    :type key: str
    :param type: Difference type (added, deleted, unchanged,
                      modified or nested).
    :param value_old: The old value associated with the key (optional).
    :type value_old: any
    :param value_new: The new value associated with the key (optional).
    :type value_new: any
    :param children: The nested difference tree for a nested difference
                     (optional).
    :type children: list
    :return: A dictionary representing the difference tree node.
    :rtype: dict
    """
    node = {'key': key, 'type': type}

    if value_old is not None:
        node['value_old'] = value_old

    if value_new is not None:
        node['value_new'] = value_new

    if children is not None:
        node['children'] = children

    return node


def format_value(data):
    """
    This function takes values in dictionaries
    and converts it to a string representation other than integer.
    Dictionaries and their values are processed recursively.
    :param data: The value to be converted to a string.
    :type data: any
    :return: A string representation of a value or a dictionary.
    :rtype: str or dict
    """
    nested_dict = {}

    if isinstance(data, bool):
        return str(data).lower()

    elif data is None:
        return 'null'

    elif isinstance(data, int):
        return data

    elif isinstance(data, dict):
        for key in data:
            nested_dict[key] = format_value(data[key])

    else:
        return str(data)

    return nested_dict
