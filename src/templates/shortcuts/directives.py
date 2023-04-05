import pathlib as plib

from kivy.lang import Builder

def include(py_file_path: str):
    kv_file_path = plib.Path(py_file_path).with_suffix('.kv')
    Builder.load_file(str(kv_file_path))
