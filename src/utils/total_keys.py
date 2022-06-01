def total_keys_util(test_dict):
    return (
        0
        if not isinstance(test_dict, dict)
        else len(test_dict) + sum(total_keys_util(val) for val in test_dict.values())
    )
