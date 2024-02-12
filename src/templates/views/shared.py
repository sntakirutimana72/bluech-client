from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from ...utils.workers import Worker

class View(Widget):
    app = ObjectProperty(allownone=True)
    root = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._on_register_observables()

    def _on_register_observables(self, timeout=0.):
        Clock.schedule_once(lambda _: self._register_observables(), timeout)

    def _register_observables(self):
        if self.app is None:
            self._on_register_observables(timeout=1/4)
        elif hasattr(self, 'observables'):
            worker: Worker = self.app.worker
            for observable in self.observables:
                observer = getattr(self, observable)
                observer_cb = lambda *_, **kwargs: observer(**kwargs)
                worker.fbind(observable, observer_cb)

class Page(View, Screen):
    ...
