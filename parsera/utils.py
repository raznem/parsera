def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def has_any_non_none_values(input_data: dict | list) -> bool:
    """
    Recursively checks if an arbitrarily nested dictionary or list contains any non-None values.

    Args:
        input_data (dict or list): The dictionary or list to check. Can be nested.

    Returns:
        bool: True if the data structure (or any nested structure) contains at least one value
              that is not None, False otherwise (i.e., all values are None or containers
              that ultimately only contain None).
    """
    if isinstance(input_data, dict):
        for value in input_data.values():
            if value is not None:
                if not isinstance(value, (dict, list)):
                    return True
                elif has_any_non_none_values(value):
                    return True

    elif isinstance(input_data, list):
        for item in input_data:
            if item is not None:
                if not isinstance(item, (dict, list)):
                    return True
                elif has_any_non_none_values(item):
                    return True

    return False
