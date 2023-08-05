

def snake(name: str) -> str:
    """
    Snake convert camel case to snake case
    :param name: camel case
    :return: snake case
    """
    name = name[0].lower() + name[1:]

    result = ""
    for char in name:
        if char.isupper():
            result += "_"
        result += char.lower()
    return result
