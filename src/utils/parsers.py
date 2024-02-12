import pathlib
import yaml

from .logger import Logger

# noinspection PyUnboundLocalVariable
class YMLParser:
    def __init__(self, filename: pathlib.Path, loader=None):
        self.filename = filename
        self.loader = loader or yaml.FullLoader
        self._yml = None

    def load(self):
        with self.filename.open(mode='r') as yml:
            self._yml = yaml.load(yml, Loader=self.loader)
        return self

    def fetch(self, name: str):
        try:
            main_key, sec_key = name.split('/')
            value = self._yml[main_key][sec_key]
        except:
            Logger.error().raises()
        return value

    def block(self, name: str):
        try:
            value = self._yml[name]
        except:
            Logger.error().raises()
        return value

    @property
    def yml(self):
        return self._yml
