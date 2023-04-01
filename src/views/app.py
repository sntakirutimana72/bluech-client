from kivy.app import App

from .dashboard import Dashboard

class BluechClientApp(App):
    def build(self):
        return Dashboard()
