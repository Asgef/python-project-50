import itertools


TEMPLATE_STYLISH = '{}  {}{}: {}'
TEMPLATE_NESTED = '{}    {}: {}'


def diff_stylish_format(data, depth=0):
    lines = []
    indent_char = '    '
    indent = indent_char * depth
    data.sort(key=lambda node: node['key'])

    for node in data:
        if node['status'] == 'nested':
            lines.extend(format_node(node, depth, indent))
        else:
            lines.extend(format_node(node, depth, indent))

    result = itertools.chain('{', lines, [indent + '}'])
    return '\n'.join(result)


def format_node(data, depth, indent):
    line = []
    step = 1
    if data['status'] == 'added':
        line.append(line_format(data['key'], data['value_new'], depth, '+ '))
    elif data['status'] == 'removed':
        line.append(line_format(data['key'], data['value_old'], depth, '- '))
    elif data['status'] == 'changed':
        line.append(line_format(data['key'], data['value_old'], depth, '- '))
        line.append(line_format(data['key'], data['value_new'], depth, '+ '))
    elif data['status'] == 'unchanged':
        line.append(line_format(data['key'], data['value_old'], depth, '  '))
    elif data['status'] == 'nested':
        line.append(
            TEMPLATE_STYLISH.format(indent, '  ', data['key'],
                                    diff_stylish_format(
                                        data['children'],
                                        depth + step
                                    )
                                    )
        )

    return line


def line_format(key, value, depth, char):
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


def dict_format(data, depth):
    indent_char = '    '
    indent = indent_char * depth
    line = []

    for key, value in sorted(data.items()):
        line.append(line_format(key, value, depth, '  '))
    result = itertools.chain('{', line, [indent + '}'])

    return '\n'.join(result)
