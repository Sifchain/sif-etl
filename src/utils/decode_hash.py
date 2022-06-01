import base64


def decode_hash_util(hash_str):
    if hash_str is None:
        return None
    return (base64.b64decode(hash_str)).decode('UTF-8')
