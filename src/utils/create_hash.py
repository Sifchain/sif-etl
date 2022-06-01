import hashlib


def create_hash_util(message, timestamp):
    hash = message + timestamp
    hash = hashlib.md5(hash.encode('utf-8')).hexdigest()[:16]
    return hash
