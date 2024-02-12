from kivy.uix.label import Label
from kivy.properties import StringProperty, ColorProperty

from .behaviors import Clicking, Hovering
from .layouts import GUILayout
from ..utils.directives import include

include(__file__)

class CButton(Clicking, Hovering, GUILayout):
    hovering_color = ColorProperty('purple')
    clicking_color = ColorProperty('cyan')

    def swap_vals(self, prop_c: str, prop_x: str):
        c_old_value = getattr(self, prop_c)
        x_old_value = getattr(self, prop_x)

        setattr(self, prop_c, x_old_value)
        setattr(self, prop_x, c_old_value)

    def _on_click(self):
        self.swap_vals('background_color', 'clicking_color')

    def _on_hover(self):
        self.swap_vals('background_color', 'hovering_color')

    def on_release(self):
        self._on_click()

    def on_press(self):
        self._on_click()

    def on_enter(self):
        self._on_hover()

    def on_leave(self):
        self._on_hover()

class PrimaryButton(CButton, Label):
    disabled_color = ColorProperty('gray')
    text = StringProperty('Click Me!')
