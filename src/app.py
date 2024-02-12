from kivy.properties import DictProperty, OptionProperty, BooleanProperty
from kivy.app import App

from .settings import (
    COMMON_KV_TEMPLATES, APP_TITLE, DEFAULT_THEME, THEMES, DEFAULT_THEME_FILENAME, THEMES_PATH,
)
from .templates.views.dashboard import Dashboard
from .utils.parsers import YMLParser
from .utils.directives import include
from .utils.workers import Worker
from .utils.jobs import AuthJobs

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
    theme = OptionProperty(DEFAULT_THEME, options=THEMES)
    themes_ctx = DictProperty({})

    def change_theme(self):
        old_theme_index = THEMES.index(self.theme)
        new_index = len(THEMES) - old_theme_index - 1
        self.theme = THEMES[new_index]

    def on_theme(self, *args):
        yml = YMLParser(THEMES_PATH / DEFAULT_THEME_FILENAME).load()
        self.themes_ctx |= yml.block(args[1])

class BluechApp(UserContextProvider, ThemeContextProvider):
    title = APP_TITLE

    _synced = BooleanProperty()
    """It holds the status of the endpoints server in global scope throughout the app lifetime."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        include(COMMON_KV_TEMPLATES)

        self.worker = Worker()
        self.worker.bind(on_signed_out=self._on_signed_out)
        self.root = Dashboard(app=self)

    def on_start(self):
        self.worker.ignite()

    def sign_out(self):
        self.root.signing_out()
        worker = self.worker
        worker.post_job_safely(AuthJobs.signout())

    def _on_signed_out(self, *args):
        self.root.signed_out(args[1]['status'])

    @property
    def synced(self):
        return self._synced

    @synced.setter
    def synced(self, state: bool):
        self._synced = state
