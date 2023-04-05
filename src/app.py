from kivy.app import App

from .workers import Worker
from .views import Dashboard

class BluechClientApp(App):
    def build(self):
        return Dashboard(worker=Worker())
