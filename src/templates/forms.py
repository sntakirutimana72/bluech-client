from kivy.properties import ObjectProperty, StringProperty

from .fields import TextField
from .progress_elements import RingSpin
from .layouts import Grid
from .buttons import PrimaryButton
from ..utils.directives import include

include(__file__)

class LogonForm(Grid):
    __events__ = 'on_submit',

    username: TextField = ObjectProperty()
    password: TextField = ObjectProperty()
    submit_btn: PrimaryButton = ObjectProperty()
    title = StringProperty('[i][font=Comic]b[color=#0cf]lue[/color]ch[/font][/i] [b]Logon[/b]')

    def pre_submit(self):
        self.flag_form(True)
        sibling = self.submit_btn.parent.children[0]
        ring_spin = RingSpin()
        sibling.add_widget(ring_spin)
        ring_spin.spin()
        self.dispatch('on_submit')

    def post_submit(self, **kwargs):
        sibling = self.submit_btn.parent.children[0]
        ring_spin: RingSpin = sibling.children[0]
        ring_spin.halt()
        sibling.remove_widget(ring_spin)
        self.flag_form(kwargs['is_disabled'])

    def on_submit(self):
        """Triggered when the form is submitted."""

    def on_ssid_change(self, new_val: str):
        """Isolate live updates to :attr:`username`."""
        self.flag_submit(new_val, self.password.value)

    def on_password_change(self, new_val: str):
        """Isolate live updates to :attr:`password`."""
        self.flag_submit(self.password.value, new_val)

    def flag_submit(self, usr: str, usr_pass: str):
        self.submit_btn.disabled = not (usr and usr_pass)

    def flag_form(self, is_disable: bool):
        self.username.disabled = \
            self.password.disabled = \
            self.submit_btn.disabled = is_disable
