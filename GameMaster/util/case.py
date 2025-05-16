import re


camel_pat = re.compile(r"([A-Z])")
snake_pat = re.compile(r"_([a-z])")


def camel_to_snake(name: str) -> str:
    return camel_pat.sub(lambda x: "_" + x.group(1).lower(), name)


def snake_to_camel(name: str) -> str:
    return snake_pat.sub(lambda x: x.group(1).upper(), name)
