import sys
import os

from ..settings import DYNAMIC_IMPORTS

def configure_framework_logging_system():
    """
    resets some kivy internal configurations for custom reconfigurations to take effects

    ... disables kivy default file logging
    ... disables kivy console logging
    ... exclude kivy environment configuration files
    """

    # disable kivy internal logging
    os.environ["KIVY_NO_FILELOG"] = "1"
    # disable console logging
    os.environ["KIVY_NO_CONSOLELOG"] = "1"
    # disable reading configuration from environment variables
    os.environ["KIVY_NO_ENV_CONFIG"] = "1"

# noinspection PyUnresolvedReferences,PyProtectedMember
def configure_system_source_for_compiled_version():
    """
    redirects system resources lookup to an OS-based temp mounted directory
    """
    if getattr(sys, "frozen", False):
        os.chdir(sys._MEIPASS)

def configure_app_window_on_startup():
    """
    apply new kivy app window custom configuration
    """
    import pyautogui as gui

    from kivy.config import Config

    from src.helpers.cfg_getter import cfg_getter
    from src.helpers.logger import Logger

    try:
        def get_configs(*startup_configs):
            width, height = gui.size()  # System Size
            ration_w = int(width * .75)
            ration_h = int(height * .75)
            left = (width - ration_w) // 2  # X-axis
            top = (height - ration_h) // 2 - 20  # Y-axis

            yield from [
                *startup_configs,
                ('minimum_height', f'{ration_h}'), ('minimum_width', f'{ration_w}'),
                ('height', f'{ration_h}'), ('width', f'{ration_w}'),
                ('left', f'{left}'), ('top', f'{top}')
            ]

        for option, _ in get_configs(*cfg_getter('startup')):
            Config.set('graphics', option, _)

    except:
        Logger.error()
        sys.exit(1)

# Purposely for dynamic import lookup
__name__ = DYNAMIC_IMPORTS['app.uix']
