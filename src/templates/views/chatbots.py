from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout

from .shared import Page, View
from .managers import BotsManager
from ..layouts import Grid
from ..buttons import CButton
from ...utils.directives import include
from ...types import UserInterface, UserInterfaceType

include(__file__)

class BotsUsers(View, Grid):
    observables = ('on_connected', 'on_disconnected',)

    def on_connected(self, *users):
        ...

    def on_disconnected(self, **user):
        ...

class ChatBots(Page):
    observables = ('on_message',)

    users: BotsUsers = ObjectProperty()
    manager: BotsManager = ObjectProperty()

    def on_message(self, **message):
        ...

    def navigate_to(self, **user):
        self.manager.navigate_to(user)

class BotUser(CButton, BoxLayout):
    user: UserInterfaceType = DictProperty(UserInterface)
    chat_bots: ChatBots = ObjectProperty()

    def on_press(self):
        super().on_press()
        self.ids.nickname.color = 'black'
        self.chat_bots.navigate_to(**self.user)

    def on_release(self):
        super().on_release()
        self.ids.nickname.color = 'white'
