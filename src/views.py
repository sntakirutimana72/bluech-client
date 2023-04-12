from kivy.properties import ColorProperty, StringProperty, ObjectProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import rgba

from .helpers.workers import Worker
from .templates.shortcuts.directives import include
from .templates.behaviors.layouts import BLayout

include(__file__)

class View(Widget):
    app = ObjectProperty()

    def __init__(self, app=None, **kwargs):
        super(View, self).__init__(**kwargs)
        self.app = app
        self.register_listeners()

    def register_listeners(self):
        if self.app is None:
            Clock.schedule_once(lambda _: self.register_listeners())
        elif hasattr(self, '__events__'):
            worker: Worker = self.app.worker
            for event in self.__events__:
                handler = getattr(self, event)
                worker.fbind(event, handler)

class Page(View, Screen):
    widget = ObjectProperty()

class IndexPage(Page):
    __events__ = 'on_status',

    name = StringProperty('index_page')
    animation = ObjectProperty(allownone=True)
    animation_angle = NumericProperty(0)
    needle_normal_color = ColorProperty(rgba('#a5ff00ff'))
    needle_idle_color = ColorProperty(rgba('#00000000'))
    needle_color = ColorProperty(rgba('#00000000'))
    needle_cover_color = ColorProperty(rgba('#0e1574ff'))
    needle_trim = NumericProperty(2)

    def schedule_animation(self):
        self.animation = Clock.schedule_interval(lambda _: self.animate_motion(), 1/50)

    def stop_animation(self):
        if pulse := self.animation:
            pulse.cancel()
            self.animation = None
            self.needle_color = self.needle_idle_color

    def on_parent(self, _, parent):
        if parent is None:
            self.stop_animation()

    def on_status(self, *_, **kwargs):
        self.schedule_animation() if kwargs['status'] == 'Connecting' else self.stop_animation()

    def animate_motion(self):
        self.needle_color = self.needle_normal_color
        self.animation_angle -= 10

class PagesManager(ScreenManager):
    ...

class Dashboard(View, BLayout):
    __events__ = (
        'on_connected',
        'on_disconnected',
        'on_response',
    )
    background_color = ColorProperty(rgba('#0e1574ff'))
    manager: PagesManager = ObjectProperty()

    def on_connected(self, **kwargs):
        ...

    def on_disconnected(self, **kwargs):
        ...

    def on_response(self, **kwargs):
        ...
