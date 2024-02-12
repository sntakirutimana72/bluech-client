import datetime as dt
import logging
import traceback as trace

from ..settings import TEMP_APPDATA_PATH

class Logger:
    logger: logging.Logger

    @classmethod
    def setup_logger(cls):
        logfile_name = dt.datetime.now().strftime('%m_%Y')
        logging.basicConfig(
            filename=TEMP_APPDATA_PATH.joinpath('logs', f'{logfile_name}.log'),
            format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
        cls.logger = logging.getLogger('bluech-client')
        cls.logger.setLevel(logging.DEBUG)

    @staticmethod
    def raises(message='FALL THROUGH'):
        raise message

    @classmethod
    def info(cls, payload):
        cls.logger.info(str(payload))
        return cls

    @classmethod
    def critical(cls, payload):
        cls.logger.critical(str(payload))
        return cls

    @classmethod
    def warning(cls, payload):
        cls.logger.warning(str(payload))
        return cls

    @classmethod
    def error(cls, payload=None):
        if payload is None:
            payload = trace.format_exc()
        cls.logger.error(str(payload))
        return cls
