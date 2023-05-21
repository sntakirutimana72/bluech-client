from kivy.properties import ObjectProperty, DictProperty, OptionProperty, BooleanProperty
from kivy.app import App

from .settings import COMMON_KV_TEMPLATES, APP_TITLE
from .templates.views.dashboard import Dashboard
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
    theme = OptionProperty('blue', options=['blue', 'light', 'dark'])
    theme_cls = ObjectProperty()

class BluechApp(UserContextProvider, ThemeContextProvider):
    title = APP_TITLE

    _synced = BooleanProperty()
    """It holds the status of the endpoints server in global scope throughout the app lifetime."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        include(COMMON_KV_TEMPLATES)

        self.worker = Worker()
        self.root = Dashboard(app=self)

    def on_start(self):
        self.worker.ignite()

    def sign_out(self):
        self.root.signing_out()
        worker = self.worker
        worker.post_job_safely(AuthJobs.signout())

    @property
    def synced(self):
        return self._synced

    @synced.setter
    def synced(self, state: bool):
        self._synced = state
