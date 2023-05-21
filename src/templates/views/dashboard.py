import typing as ty

from kivy.properties import ColorProperty, ObjectProperty, DictProperty
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

    def replace_with(self, page: str | Page):
        if isinstance(page, str):
            page = self.discover_page(page)
        old_page = self.current_screen
        self.switch_to(page)
        self.remove_widget(old_page)

    def discover_page(self, name: str):
        if name in self.screen_names:
            return self.get_screen(name)
        return self.get_new_page(name)

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
    _tmp_stash = DictProperty({})
    background_color = ColorProperty('#0e1574ff')

    def connection_established(self):
        self.app.synced = True
        self.manager.replace_with('logon')

    def signed_in(self, user):
        self.app.signed_in(**user)
        self.manager.replace_with('welcome')

    def signing_out(self):
        self._tmp_stash['BEFORE_LOGOUT_PG'] = self.manager.current_screen
        self.manager.replace_with('logout')

    def on_signed_out(self, **kwargs):
        status_code = kwargs['status']

        if status_code == 200:
            del self._tmp_stash['BEFORE_LOGOUT_PG']
            pg_name = 'logon' if self.app.synced else 'index'
            self.manager.replace_with(pg_name)
        else:
            before_logout_pg = self._tmp_stash.pop('BEFORE_LOGOUT_PG')
            self.manager.replace_with(before_logout_pg)

    def on_response(self, **kwargs):
        ...
