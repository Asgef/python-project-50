from itertools import chain
from gendiff.formatters.templates import TEMPLATE_STYLISH


INDENT_CHAR = '    '
STEP = 1


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
    indent = INDENT_CHAR * depth

    lines = [line for node in data for line in format_node(node, depth)]

    result = chain('{', lines, [indent + '}'])

    return '\n'.join(result)


def format_node(data: dict, depth: int) -> list:
    """
   Format the node in a "stylish" format.

    This function formats the node representing the difference and returns
    a list of strings representing the difference lines for a node in
    "stylish" format.

   :param data: Node representing a difference.
   :type data: dict
   :param depth: Current depth level.
   :type depth: int
   :return: List of strings representing the difference lines for the node
            in "stylish" format.
   :rtype: list
   """
    line = []
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

        nest_indent = INDENT_CHAR * (depth + STEP)

        nested_lines = [
            line
            for child in data['children']
            for line in format_node(child, depth + STEP)
        ]

        nested_block = '\n'.join(nested_lines)
        line.append(
            f'{nest_indent}{data["key"]}: {{\n{nested_block}\n{nest_indent}}}'
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
    indent = INDENT_CHAR * depth
    line = []

    if isinstance(value, dict):
        line.append(TEMPLATE_STYLISH.format(
            indent, char, key, dict_format(value, depth + STEP))
        )

    else:
        line.append(TEMPLATE_STYLISH.format(
            indent, char, key, format_value(value))
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
    indent = INDENT_CHAR * depth
    line = []

    for key, value in data.items():
        line.append(line_format(key, value, depth, '  '))

    result = chain('{', line, [indent + '}'])

    return '\n'.join(result)


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

    elif isinstance(data, dict):
        for key in data:
            nested_dict[key] = format_value(data[key])

    else:
        return data

    return nested_dict
