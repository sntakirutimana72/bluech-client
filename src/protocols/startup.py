import pyautogui as gui

from kivy.config import Config

from ..helpers.cfg_getter import cfg_getter

def routine_002():
    width, height = gui.size()                  # System Size
    ration_w = int(width * .75)
    ration_h = int(height * .75)
    left = (width - ration_w) // 2        # X-axis
    top = (height - ration_h) // 2 - 20  # Y-axis

    return [
        ('minimum_height', f'{ration_h}'), ('minimum_width', f'{ration_w}'),
        ('height', f'{ration_h}'), ('width', f'{ration_w}'),
        ('left', f'{left}'), ('top', f'{top}')
    ]

def routine_001():
    """ configuring window from configuration file & :function:routine_002"""
    for option, _ in (cfg_getter('startup') + routine_002()):
        Config.set('graphics', option, _)
