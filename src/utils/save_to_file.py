import json


def save_to_file_util(json_obj, argv):
    try:
        file_name = argv[2]
    except:
        file_name = "default.json"

    json_obj = json.dumps(json_obj)
    with open(file_name, "w") as f:
        f.write(json_obj)
