from kivy.uix.label import Label
from kivy.properties import ListProperty, StringProperty, ColorProperty

from .behaviors import Clicking, Hovering
from ..utils.directives import include

include(__file__)

class PrimaryButton(Clicking, Hovering, Label):
    border_radius = ListProperty([4, 4, 4, 4])
    background_color = ColorProperty('#40ff88ff')
    disabled_color = ColorProperty('gray')
    text = StringProperty('Click Me!')
