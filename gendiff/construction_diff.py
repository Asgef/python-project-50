def add_node(key, status, value_old=None, value_new=None, children=None):
    node = {'key': key, 'status': status}

    if value_old is not None:
        node['value_old'] = value_old

    if value_new is not None:
        node['value_new'] = value_new

    if children is not None:
        node['children'] = children

    return node


def create_diff(file1, file2):
    diff = []
    keys = sorted(file1.keys() | file2.keys())

    for key in keys:
        if key in file1 and key not in file2:
            node = add_node(key, 'removed', value_old=file1[key])
        elif key not in file1 and key in file2:
            node = add_node(key, 'added', value_new=file2[key])
        elif file1[key] == file2[key]:
            node = add_node(key, 'unchanged', value_old=file1[key])
        elif isinstance(file1[key], dict) and isinstance(file2[key], dict):
            child = create_diff(file1[key], file2[key])
            node = add_node(key, 'nested', children=child)
        else:
            node = add_node(
                key, 'changed', value_old=file1[key], value_new=file2[key]
            )

        diff.append(node)
    return diff
