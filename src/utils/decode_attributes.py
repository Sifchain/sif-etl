import base64


def decode_attributes_util(event_attributes):
    decoded_attributes = {}
    for attribute in event_attributes:
        decoded_key = base64.b64decode(attribute["key"]).decode("utf-8")
        decoded_value = base64.b64decode(attribute["value"]).decode("utf-8")
        decoded_attributes[decoded_key] = decoded_value
    return decoded_attributes
