import datetime as dt
import logging
import traceback as trace

from ..settings import BASE_DIR

class Logger:
    logger: logging.Logger

    @classmethod
    def setup_logger(cls):
        logfile_name = dt.datetime.now().strftime('%B-%Y')
        logging.basicConfig(
            filename=BASE_DIR.joinpath('res', 'logs', f'{logfile_name}.log'),
            format='%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s')
        cls.logger = logging.getLogger('bluech-client')
        cls.logger.setLevel(logging.DEBUG)

    @classmethod
    def info(cls, payload):
        cls.logger.info(str(payload))

    @classmethod
    def critical(cls, payload):
        cls.logger.critical(str(payload))

    @classmethod
    def warning(cls, payload):
        cls.logger.warning(str(payload))

    @classmethod
    def error(cls, payload=None):
        if payload is None:
            payload = trace.format_exc()
        cls.logger.error(str(payload))
