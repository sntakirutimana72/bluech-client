import pathlib as plib

from kivy.lang import Builder

from ..settings import KV_TEMPLATES_DIR, STATIC_PATH

def include(py_file_path: str | list[str] | tuple[str]):
    if isinstance(py_file_path, (list, tuple)):
        [include(kv_file) for kv_file in py_file_path]
    else:
        kv_name = plib.Path(py_file_path).with_suffix('.kv').name
        Builder.load_file(str(KV_TEMPLATES_DIR.joinpath(kv_name)))

class StaticSRCLoader:
    @staticmethod
    def images_path():
        return STATIC_PATH / 'images'

    @classmethod
    def image(cls, stem: str, suffix='png'):
        full_path = cls.images_path() / f'{stem}.{suffix}'
        return str(full_path)
