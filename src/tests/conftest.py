# *********************
# Configure custom logging before pytest start execution and environment setup
#
from src.utils.logger import Logger
from src.protocols import (
    configure_framework_logging_system, configure_system_source_for_compiled_version,
    configure_app_window_on_startup,
)

configure_framework_logging_system()
configure_system_source_for_compiled_version()
Logger.setup_logger()
Logger.info('Starting application')
Logger.info('Engage startup protocol')
configure_app_window_on_startup()
Logger.info('Startup protocol engaged successfully.')

# *********************
