import itertools
from gendiff.formatters.templates import TEMPLATE_STYLISH


def diff_stylish_format(data: list, depth: int = 0) -> str:
    """
    Recursively format the difference tree into a "stylish" formatted string.

    This function iterates through the difference tree nodes and returns a
    string representation of the differences in the "stylish" format. It uses
    indentation to represent nested structures.

    :param data: Difference tree node or subtree as a list of dictionaries.
    :type data: list
    :param depth: Current depth level for indentation (optional).
    :type depth: int
    :return: String representation of the difference in "stylish" format.
    :rtype: str
    """
    indent_char = '    '
    indent = indent_char * depth
    data.sort(key=lambda node: node['key'])

    lines = [line for node in data for line in format_node(node, depth, indent)]

    result = itertools.chain('{', lines, [indent + '}'])

    return '\n'.join(result)


def format_node(data: dict, depth: int, indent: str) -> list:
    """
   Format the node in a "stylish" format.

    This function formats the node representing the difference and returns
    a list of strings representing the difference lines for a node in
    "stylish" format.

   :param data: Node representing a difference.
   :type data: dict
   :param depth: Current depth level.
   :type depth: int
   :param indent: Indentation string for the current depth level.
   :type indent: str
   :return: List of strings representing the difference lines for the node
            in "stylish" format.
   :rtype: list
   """
    line = []
    step = 1
    if data['type'] == 'added':
        line.append(line_format(
            data['key'], data['value_new'], depth, '+ ')
        )

    elif data['type'] == 'removed':
        line.append(
            line_format(data['key'], data['value_old'], depth, '- ')
        )

    elif data['type'] == 'changed':
        line.append(
            line_format(data['key'], data['value_old'], depth, '- ')
        )
        line.append(
            line_format(data['key'], data['value_new'], depth, '+ ')
        )

    elif data['type'] == 'unchanged':
        line.append(
            line_format(data['key'], data['value_old'], depth, '  ')
        )

    elif data['type'] == 'nested':
        line.append(
            TEMPLATE_STYLISH.format(
                indent, '  ', data['key'],
                diff_stylish_format(data['children'], depth + step)
            )
        )

    return line


def line_format(key: str, value: any, depth: int, char: str) -> str:
    """
    Format a line in the "stylish" format.

    This function formats a line representing a difference and returns a
    string representation for the line in "stylish" format.

    :param key: Key representing the difference.
    :type key: str
    :param value: Value associated with the key.
    :type value: any
    :param depth: Current depth level.
    :type depth: int
    :param char: Symbol representing the type of difference.
    :type char: str
    :return: String representation of the line in "stylish" format.
    :rtype: str
    """
    indent_char = '    '
    indent = indent_char * depth
    step = 1
    line = []

    if isinstance(value, dict):
        line.append(TEMPLATE_STYLISH.format(
            indent, char, key, dict_format(value, depth + step))
        )

    else:
        line.append(TEMPLATE_STYLISH.format(
            indent, char, key, value)
        )

    return '\n'.join(line)


def dict_format(data: dict, depth: int):
    """
    Format a dictionary in the "stylish" format.

    This function formats a dictionary representing a nested structure and
    returns a string representation for the dictionary in "stylish" format.

    :param data: Dictionary representing the nested structure.
    :type data: dict
    :param depth: Current depth level.
    :type depth: int
    :return: String representation of the dictionary in "stylish" format.
    :rtype: str
    """
    indent_char = '    '
    indent = indent_char * depth
    line = []

    for key, value in sorted(data.items()):
        line.append(line_format(key, value, depth, '  '))

    result = itertools.chain('{', line, [indent + '}'])

    return '\n'.join(result)
