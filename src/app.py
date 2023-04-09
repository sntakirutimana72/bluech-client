from kivy.app import App
from kivy.properties import ObjectProperty

from .helpers.workers import Worker
from .views import Dashboard

class BluechClientApp(App):
    worker: Worker = ObjectProperty()

    def build(self):
        self.worker = Worker()
        root_widget = Dashboard(app=self)

        return root_widget

    def on_start(self):
        self.worker.ignite()
