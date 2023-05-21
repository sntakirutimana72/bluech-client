from kivy.tests import GraphicUnitTest
from kivy.base import EventLoop
from kivy.uix.widget import Widget

from .selectors import ElementsSelector
from .utils import Mocks
from ...app import BluechApp as App
from ...templates.forms import LogonForm
from ...templates.views.shared import Page
from ...templates.views.pages import Logon
from ...templates.views.dashboard import PagesManager, Dashboard

class GUISpec(ElementsSelector):
    app: App
    form: LogonForm
    manager: PagesManager
    root: Dashboard
    current_page: Page
    window: EventLoop.window

    @property
    def root(self) -> Dashboard:
        return self.app.root

    @property
    def manager(self) -> PagesManager:
        return self.root.manager

    @property
    def current_page(self) -> Page:
        manager = self.manager
        return manager.current_screen

    def build(self):
        self.app = app = App()
        app.run()
        EventLoop.ensure_window()
        self.window = EventLoop.window

    def buildLogon(self):
        self.build()
        index = self.current_page
        index.on_status(status='online')
        form = getattr(self.current_page, 'form')
        self.assertIsInstance(form, LogonForm)
        self.form = form

class GUnittest(GUISpec, GraphicUnitTest):
    @staticmethod
    def dispatch(elem: Widget, event: str):
        elem.dispatch(event)

    def click(self, elem: Widget):
        self.dispatch(elem, 'on_press')

    def prompt_user(self, **kwargs):
        self.form.username.value = kwargs['username']
        self.form.password.value = kwargs['pass_w']

    def signInUser(self, **response):
        user = Mocks.Users.regular()
        self.prompt_user(username=user['email'], pass_w=user['pass_w'])
        self.assertFalse(self.form.submit_btn.disabled)
        self.click(self.form.submit_btn)
        self.assertTrue(self.form.submit_btn.disabled)

        logon = self.current_page
        self.assertIsInstance(logon, Logon)
        logon.on_signed_in(**response)
