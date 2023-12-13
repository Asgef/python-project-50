import itertools


def format_node(data, depth, spaces_count, replacer):
    step = 1
    offset = 2
    indent_val = replacer * (spaces_count * (depth + step) - offset)
    indent_nes = replacer * (spaces_count * (depth + step))
    if data['status'] == 'added':
        return f'\n{indent_val}+ {data["key"]}: {data["value_new"]}'
    elif data['status'] == 'removed':
        return f'\n{indent_val}- {data["key"]}: {data["value_old"]}'
    elif data['status'] == 'changed':
        return f'\n{indent_val}- {data["key"]}: {data["value_old"]}\n{indent_val}+ {data["key"]}: {data["value_new"]}'
    elif data['status'] == 'unchanged':
        return f'\n{indent_val}  {data["key"]}: {data["value_old"]}'
    else:
        return f'\n{indent_nes}{data["key"]}: {diff_format(data["children"], depth + 1, spaces_count, replacer)}'


def diff_format(data, depth=0, spaces_count=4, replacer=' '):
    indent = replacer * (depth * spaces_count)
    data.sort(key=lambda node: node['key'])
    lines = [format_node(node, depth, spaces_count, replacer) for node in data]
    result = itertools.chain('{', lines, '\n' + indent + '}')
    return ''.join(result)
