import typing as ty

from kivy.properties import ColorProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager

from . import pages
from .shared import View, Page
from ..layouts import Box
from ...utils.directives import include

include('views')

def get_page(name: str) -> ty.Type[Page] | None:
    name = name.title()
    pg = vars(pages)
    return pg.get(name)

class PagesManager(ScreenManager):
    root: View = ObjectProperty()

    def forget_and_switch(self, page: str | Page):
        if isinstance(page, str):
            page = self.get_new_page(page)
        forgotten_page = self.current_screen
        self.switch_to(page)
        self.remove_widget(forgotten_page)

    def get_new_page(self, name: str) -> Page:
        options = {'root': self.root, 'app': self.root.app}
        if page_cls := get_page(name):
            page = page_cls(**options)
        else:
            page = Page(name=name, **options)
        return page

class Dashboard(View, Box):
    __worker_events__ = 'on_signed_out', 'on_response',

    manager: PagesManager = ObjectProperty()
    background_color = ColorProperty('#0e1574ff')

    def connection_established(self):
        self.manager.forget_and_switch('logon')

    def signed_in(self, user):
        self.app.signed_in(**user)
        self.manager.forget_and_switch('welcome')

    def on_signed_out(self, **kwargs):
        self.manager.forget_and_switch('index')

    def on_response(self, **kwargs):
        ...
