from gendiff.formatters.templates import (
    TEMPLATE_PLAIN_PATH,
    TEMPLATE_PLAIN_ADDED,
    TEMPLATE_PLAIN_REMOVED,
    TEMPLATE_PLAIN_UPDATE
)


def diff_plain_format(data, source=""):
    lines = []
    data.sort(key=lambda node: node['key'])

    for node in data:
        if source:
            path = TEMPLATE_PLAIN_PATH.format(source, node['key'])
        else:
            path = node['key']

        lines.extend(format_node(node, path))

    return '\n'.join(lines)


def format_node(data, path):
    line = []

    if data['status'] == 'added':
        line.append(
            TEMPLATE_PLAIN_ADDED.format(
                path,
                format_val(data['value_new'])
            )
        )

    elif data['status'] == 'removed':
        line.append(
            TEMPLATE_PLAIN_REMOVED.format(path)
        )

    elif data['status'] == 'changed':
        line.append(
            TEMPLATE_PLAIN_UPDATE.format(
                path,
                format_val(data['value_old']),
                format_val(data['value_new'])
            )
        )

    elif data['status'] == 'nested':
        line.append(
            diff_plain_format(data['children'], path)
        )

    return line


def format_val(data):

    if isinstance(data, dict):
        return '[complex value]'

    elif data in ['false', 'true', 'null']:
        return data

    elif isinstance(data, str):
        return "'{}'".format(data)

    elif isinstance(data, int):
        return "{}".format(data)
