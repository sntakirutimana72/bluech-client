from kivy.properties import ColorProperty

from .shortcuts.directives import include
from .templates.layouts import BLayout

include(__file__)

class Dashboard(BLayout):
    background_color = ColorProperty([0, 0, 1, .4])
