from kivy.properties import ColorProperty, StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from .workers import Worker
from .templates.shortcuts.directives import include
from .templates.behaviors.layouts import BLayout

include(__file__)

class View(object):
    def __init__(self, worker: Worker):
        self.worker = worker
        self.register_listeners()

    def register_listeners(self):
        if hasattr(self, '__events__'):
            for event in self.__events__:
                handler = getattr(self, event)
                self.worker.fbind(event, handler)

class Page(Screen, View):
    app = ObjectProperty()
    widget = ObjectProperty()

class IndexPage(Page):
    __events__ = 'on_status',

    name = StringProperty('index_page')

    def on_status(self, status=None):
        ...

class PagesManger(ScreenManager):
    ...

class Dashboard(BLayout, View):
    __events__ = (
        'on_connected',
        'on_disconnected',
        'on_response',
    )
    background_color = ColorProperty([0, 0, 1, .4])
    manager: PagesManger = ObjectProperty()

    def on_connected(self, **kwargs):
        ...

    def on_disconnected(self, **kwargs):
        ...

    def on_response(self, **kwargs):
        ...
