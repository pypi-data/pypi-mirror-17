import asyncio


def get(key, default=None):
    """
    Retrieves the value stored in key from the Task.context dict. If key does not exist,
    default will be returned

    :param key: identifier for accessing the context dict.
    :param default: None by default, returned in case key is not found.
    :return: Value stored inside the dict[key].
    """
    try:
        return asyncio.Task.current_task().context[key]
    except (KeyError, AttributeError):
        return default


def set(key, value):
    """
    Sets the given value inside Task.context[key]. If the key does not exist it creates it.

    :param key: identifier for accessing the context dict.
    :param value: value to store inside context[key].
    """
    try:
        asyncio.Task.current_task().context[key] = value
    except AttributeError:
        asyncio.Task.current_task().context = {key: value}
