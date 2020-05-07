import json
from copy import deepcopy

def write_json(filename, data):
    """ Write to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f)


def read_json(filename):
    """ Read from JSON file"""
    with open(filename) as data_file:
        return json.load(data_file)

def drop_item(d, value=None, key=None):
    """ Drop item from a dict given its key or value """
    d = deepcopy(d)
    return {k: v for (k, v) in d.items() if k != key and v != value}
