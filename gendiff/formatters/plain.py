TEMPLATE_PLAIN_PATH = '{}.{}'
TEMPLATE_PLAIN_ADDED = "Property '{}' was added with value: {}"
TEMPLATE_PLAIN_REMOVED = "Property '{}' was removed"
TEMPLATE_PLAIN_UPDATE = "Property '{}' was updated. From {} to {}"


def diff_plain_format(data, source=""):
    lines = []
    data.sort(key=lambda node: node['key'])

    for node in data:
        if source:
            path = TEMPLATE_PLAIN_PATH.format(source, node['key'])
        else:
            path = node['key']

        lines.extend(format_node(node, path))

    result = '\n'.join(lines)
    return result


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
