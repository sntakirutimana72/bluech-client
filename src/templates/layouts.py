from kivy.properties import ListProperty, ColorProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from ..utils.directives import include

include(__file__)

class GUILayout(Widget):
    border_radius = ListProperty([4, 4, 4, 4])
    background_color = ColorProperty('#0d18a550')

class Grid(GUILayout, GridLayout):
    ...

class Box(GUILayout, BoxLayout):
    ...
