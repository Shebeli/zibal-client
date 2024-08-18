def convert_to_camel_case(snake_str: str) -> str:
    """Converts a snake case string to camel case"""
    words = snake_str.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def to_camel_case_dict(data: dict) -> dict:
    """Converts snake case keys of a dict into camel case."""
    return {convert_to_camel_case(k): v for k, v in data.items()}


def convert_to_snake_case(camel_str: str) -> str:
    """Converts a camel case string to snake case."""
    words = []
    j = 0  # previous word starting index pointer

    for i in range(len(camel_str)):
        if camel_str[i].isupper():
            words.append(camel_str[j:i].lower())
            j = i

    # append the last remaining word
    words.append(camel_str[j:].lower())
    return "_".join(words)


def to_snake_case_dict(data: dict) -> dict:
    """Converts camel case keys of a dict into snake case."""
    return {convert_to_snake_case(k): v for k, v in data.items()}
