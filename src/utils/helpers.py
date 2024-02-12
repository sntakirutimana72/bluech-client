import pathlib

def isnumber(value):
    if isinstance(value, (float, int)):
        return True
    if isinstance(value, str):
        return value.isdigit()

def with_sfx(stem: str, suffix: str):
    return str(pathlib.Path(stem).with_suffix(suffix))

def with_yml_sfx(stem: str):
    return with_sfx(stem, '.yml')
