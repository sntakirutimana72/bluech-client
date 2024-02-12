import pathlib as plib

from kivy.lang import Builder

from ..settings import KV_TEMPLATES_DIR, STATIC_PATH, ASSETS_PATH

def include(py_file_path: str | list[str] | tuple[str]):
    if isinstance(py_file_path, (list, tuple)):
        [include(kv_file) for kv_file in py_file_path]
    else:
        kv_name = plib.Path(py_file_path).with_suffix('.kv').name
        Builder.load_file(str(KV_TEMPLATES_DIR.joinpath(kv_name)))

def dissect_pattern(pattern: str, scope_path: plib.Path):
    folder, file = pattern.rsplit(':', 1)
    res = scope_path.joinpath(*folder.split(':'), file)
    return res

def resource(pattern: str):
    res = dissect_pattern(pattern, ASSETS_PATH)
    return str(res)

def static(pattern: str):
    res = dissect_pattern(pattern, STATIC_PATH)
    return str(res)

def static_img(pattern: str):
    img = dissect_pattern(f'images:{pattern}', STATIC_PATH)
    if not img.suffix:
        img = img.with_suffix('.png')
    return str(img)

def half(whole_num: int | float):
    return whole_num * 0.5

def double(og_value: int | float):
    return og_value * 2

def flat(og_value, times: int = 2):
    return (og_value,) * times
