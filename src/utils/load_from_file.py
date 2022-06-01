import json


def load_from_file_util(file_name):
    with open(file_name, "r") as f:
        data = json.load(f)

    return data
