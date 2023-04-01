from kivy.app import App

from .dashboard.dashboard import Dashboard
from ..workers import CoreWorker

class BluechClientApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_loop_worker = None

    def build(self):
        return Dashboard()

    def run_worker(self):
        if self.event_loop_worker:
            return

        def display_update(instance, *largs):
            self.root.dispatch('on_update', largs[0])

        def connect_status(instance, *largs):
            self.root.dispatch('on_connect', largs[0])

        self.event_loop_worker = engine = CoreWorker()
        engine.bind(
            on_update=display_update,
            on_connect=connect_status
        )
        engine.ignite()

    def connect(self, *largs):
        node_worker = self.event_loop_worker

        if node_worker is not None:
            loop = None
            while not loop:
                loop = self.event_loop_worker.loop
            loop.call_soon_threadsafe(node_worker.connect, *largs)

    def submit_message(self, message: dict):
        node_worker = self.event_loop_worker

        loop = None
        while not loop:
            loop = self.event_loop_worker.loop
        loop.call_soon_threadsafe(node_worker.submit, message)