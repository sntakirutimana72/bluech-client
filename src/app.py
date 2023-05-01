from kivy.properties import ObjectProperty, DictProperty
from kivy.app import App

from .settings import COMMON_KV_TEMPLATES
from .templates.views import Dashboard
from .utils.directives import include
from .utils.workers import Worker

class BluechClientApp(App):
    worker: Worker = ObjectProperty()
    user = DictProperty({'is_anonymous': True})

    def build(self):
        include(COMMON_KV_TEMPLATES)
        self.worker = Worker()
        root_widget = Dashboard(app=self)

        return root_widget

    def on_start(self):
        self.worker.ignite()

    def signed_in(self, **user):
        user['is_anonymous'] = False
        self.user |= user

    def signed_out(self):
        self.user = {'is_anonymous': True}
