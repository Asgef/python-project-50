import json
import yaml


def parse(data: str, data_format: str) -> dict:
    """
    Parsing data from JSON or YAML into a dictionary.

    This function accepts data as a string and the name
    of the format to which this data belongs.
    Depending on the name of the format, JSON or YAML
    data is converted into a dictionary. The data is returned.

    :param data: Text data
    :param data_format: Format
    :return: Parsed data
    :rtype: dict
    """
    if data_format == 'json':
        return json.loads(data)
    elif data_format == 'yaml':
        return yaml.load(data, yaml.Loader)
