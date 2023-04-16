import configparser as cfg
import traceback as trace

from .logger import Logger
from ..settings import BASE_DIR

def cfg_getter(section: str, option: str | None = None):
    try:
        parser = cfg.ConfigParser()
        parser.read(BASE_DIR / 'bluech.ini')
        payload = parser.get(section, option) if option else parser.items(section)
    except:
        Logger.error(trace.print_exc())
    else:
        return payload
