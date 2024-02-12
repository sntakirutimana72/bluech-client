__name__ = 'bluech_client.protocols.startup.uix'

import sys
import os

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

    from src.settings import BASE_DIR, APP_NAME
    from src.utils.parsers import YMLParser
    from src.utils.helpers import with_yml_sfx

    def normalize_pos_size(rx: float, ry: float):
        sw, sh = gui.size()
        sx = int(sw * rx)
        sy = int(sh * ry)
        x = (sw - sx) // 2
        y = (sh - sy) // 2 - 20

        return (
            ('height', f'{sy}'),
            ('width', f'{sx}'),
            ('left', f'{x}'),
            ('top', f'{y}')
        )

    def all_configs():
        startup_block = parser.block('startup')
        s_ratios = startup_block.pop('size')

        yield from (
            *startup_block.items(),
            *normalize_pos_size(*s_ratios)
        )

    parser = YMLParser(BASE_DIR / with_yml_sfx(APP_NAME)).load()

    for option, value in all_configs():
        Config.set('graphics', option, value)
