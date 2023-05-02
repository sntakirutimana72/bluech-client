from kivy.tests import GraphicUnitTest
from kivy.base import EventLoop
from kivy.uix.widget import Widget

from .selectors import ElementsSelector
from ...app import BluechClientApp
from ...templates.views import Page, PagesManager, Dashboard

class GUISpec(ElementsSelector):
    app: BluechClientApp
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
        return manager.get_screen(manager.current)

    def build(self):
        self.app = app = BluechClientApp()
        app.run()
        EventLoop.ensure_window()
        self.window = EventLoop.window

class GUnittest(GUISpec, GraphicUnitTest):
    @staticmethod
    def dispatch(elem: Widget, event: str):
        elem.dispatch(event)

    def click(self, elem: Widget):
        self.dispatch(elem, 'on_press')
