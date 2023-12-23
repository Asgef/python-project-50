import json
import yaml


def parse(data: str, data_format: str) -> dict:
    if data_format == 'json':
        return json.loads(data)
    elif data_format == 'yaml':
        return yaml.load(data, yaml.Loader)
    else:
        raise FileNotFoundError(f'Invalid data_format: {data_format}')
