from kivy.properties import ColorProperty, ObjectProperty, DictProperty

from .shared import View
from .managers import PagesManager
from .chatbots import ChatBots
from ..layouts import Box
from ...utils.directives import include

include(__file__)

class Dashboard(View, Box):
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

    def signed_out(self, status: int):
        if status == 200:
            del self._tmp_stash['BEFORE_LOGOUT_PG']
            pg_name = 'logon' if self.app.synced else 'index'
            self.manager.replace_with(pg_name)
        else:
            before_logout_pg = self._tmp_stash.pop('BEFORE_LOGOUT_PG')
            self.manager.replace_with(before_logout_pg)
