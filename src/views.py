from kivy.properties import ColorProperty, StringProperty, ObjectProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock

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
    stat_message = StringProperty('Offline')
    motion_trigger = ObjectProperty(allownone=True)
    animation_counter = NumericProperty(0)

    def schedule_animation(self):
        self.motion_trigger = Clock.schedule_interval(lambda _: self.animate_motion(), 1/1.25)

    def stop_animation(self):
        if self.motion_trigger:
            trigger = self.motion_trigger
            self.motion_trigger = None
            trigger.cancel()

    def on_parent(self, *args):
        if args[1] is None:
            self.stop_animation()

    def on_status(self, *_, **kwargs):
        status = kwargs['status']
        if status == 'Connecting':
            self.stat_message = status
            self.schedule_animation()
        else:
            self.stop_animation()
            self.stat_message = status

    def animate_motion(self):
        counter = self.animation_counter + 1
        if counter > 3:
            counter = 0
        # noinspection PyArgumentList
        stat_message = self.stat_message.replace('.', '')
        self.stat_message = f"{stat_message}{'.' * counter}"
        self.animation_counter = counter

class PagesManager(ScreenManager):
    ...

class Dashboard(View, BLayout):
    __events__ = (
        'on_connected',
        'on_disconnected',
        'on_response',
    )
    background_color = ColorProperty([0, 0, 1, .4])
    manager: PagesManager = ObjectProperty()

    def on_connected(self, **kwargs):
        ...

    def on_disconnected(self, **kwargs):
        ...

    def on_response(self, **kwargs):
        ...
