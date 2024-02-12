import typing as ty

from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty

from .shared import Page, View
from . import pages
from ...types import UserInterfaceType

def get_page(name: str) -> ty.Type[Page] | None:
    name = name.title()
    pg = vars(pages)
    return pg.get(name)

class Manager(ScreenManager):
    root: View = ObjectProperty()

class PagesManager(Manager):
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

class BotsManager(Manager):
    def navigate_to(self, partner: UserInterfaceType):
        bot_name = self.get_bot_name(partner)
        self.discover_room(name=bot_name, partner=partner)

    def discover_room(self, **kwargs):
        if self.has_screen(kwargs['name']):
            self.current = kwargs['name']
        else:
            bot: pages.Bot = self.get_new_room(**kwargs)
            self.switch_to(bot)

    def get_new_room(self, **kwargs):
        app = self.root.app
        bot = pages.Bot(owner=app.user, **kwargs)
        app.bind(user=bot.setter('owner'))
        return bot

    @staticmethod
    def get_bot_name(user: UserInterfaceType):
        user_id = user['id']
        return f'bot#{user_id}'
