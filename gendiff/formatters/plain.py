from gendiff.formatters.templates import (
    TEMPLATE_PLAIN_PATH,
    TEMPLATE_PLAIN_ADDED,
    TEMPLATE_PLAIN_REMOVED,
    TEMPLATE_PLAIN_UPDATE
)


def diff_plain_format(data: list) -> str:
    """
    Format the difference tree in "plain" format.

    :param data: Difference tree.
    :return: A string of difference in "plain" format.
    """
    lines = [line for node in data for line in format_node(node, node['key'])]

    return '\n'.join(lines)


def format_node(data: dict, path: str) -> list:
    """
    Create a node representation in "plain" format.

    :param data: The node representing a difference.
    :type data: dict
    :param path: The path to the current node.
    :type path: str
    :return: List of strings representing the difference lines for the node
            in "plain" format.
    :rtype: list
    """
    line = []

    if data['type'] == 'added':
        line.append(
            TEMPLATE_PLAIN_ADDED.format(
                path,
                format_val(data['value_new'])
            )
        )

    elif data['type'] == 'removed':
        line.append(
            TEMPLATE_PLAIN_REMOVED.format(path)
        )

    elif data['type'] == 'changed':
        line.append(
            TEMPLATE_PLAIN_UPDATE.format(
                path,
                format_val(data['value_old']),
                format_val(data['value_new'])
            )
        )

    elif data['type'] == 'nested':
        for child in data['children']:
            nested_path = TEMPLATE_PLAIN_PATH.format(path, child['key'])
            line.extend(format_node(child, nested_path))

    return line


def format_val(data):
    """
   Convert the dictionary in value to [complex value].

   This function checks whether the value is a dictionary in the node value,
   if true it returns [complex value].
   Also substitutes string representations of the types
   bool, None and int without quotes into the template.

   :param data: The value to be converted.
   :type data: str
   :return: The string representation of the value or '[complex value]'
            if the value is a dictionary.
   :rtype: str
   """

    if isinstance(data, dict):
        return '[complex value]'

    elif isinstance(data, bool):
        return str(data).lower()

    elif data is None:
        return 'null'

    elif isinstance(data, str):
        return "'{}'".format(data)

    elif isinstance(data, int):
        return "{}".format(data)
