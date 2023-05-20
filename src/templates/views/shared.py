from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from ...utils.workers import Worker

class View(Widget):
    app = ObjectProperty(allownone=True)
    root = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)
        self.schedule_listeners_registration()

    def schedule_listeners_registration(self, timeout=0.):
        Clock.schedule_once(lambda _: self.register_listeners(), timeout)

    def register_listeners(self):
        if self.app is None:
            self.schedule_listeners_registration(timeout=1/4)
        elif hasattr(self, '__worker_events__'):
            worker: Worker = self.app.worker
            for event_uid in self.__worker_events__:
                event_handler = getattr(self, event_uid)
                callback = lambda *_, **kwargs: event_handler(**kwargs)
                worker.fbind(event_uid, callback)

class Page(View, Screen):
    ...
