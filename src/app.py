from kivy.properties import ObjectProperty, DictProperty, OptionProperty
from kivy.app import App

from .settings import COMMON_KV_TEMPLATES, APP_TITLE
from .templates.views.dashboard import Dashboard
from .utils.directives import include
from .utils.workers import Worker

class UserContextProvider(App):
    user = DictProperty({
        'is_anonymous': True,
        'nickname': 'Anonymous',
        'email': None,
        'id': None
    })

    def signed_in(self, **user):
        user['is_anonymous'] = False
        self.user |= user

    def signed_out(self):
        user = {
            'is_anonymous': True,
            'nickname': 'Anonymous',
            'email': None,
            'id': None
        }
        self.user |= user

class ThemeContextProvider(App):
    theme = OptionProperty('blue', options=['blue', 'light', 'dark'])
    theme_cls = ObjectProperty()

class BluechApp(UserContextProvider, ThemeContextProvider):
    title = APP_TITLE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        include(COMMON_KV_TEMPLATES)

        self.worker = Worker()
        self.root = Dashboard(app=self)

    def on_start(self):
        self.worker.ignite()
