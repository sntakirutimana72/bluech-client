from kivy.properties import ListProperty, ColorProperty, BooleanProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from ..utils.directives import include, static

include(__file__)

class GUILayout(Widget):
    border_radius = ListProperty([4, 4, 4, 4])
    background_color = ColorProperty('#f5f6fa')

class Icon(Widget):
    is_circular = BooleanProperty(False)
    border = ListProperty([4, 4, 4, 4])
    background_color = ColorProperty('white')
    source = StringProperty('')
    name = StringProperty('')

    def on_name(self, *args):
        if args[1]:
            self.source = static(f'images:{args[1]}')
        else:
            self.source = ''

class Grid(GUILayout, GridLayout):
    ...

class Box(GUILayout, BoxLayout):
    ...
