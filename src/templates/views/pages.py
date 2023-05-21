from kivy.properties import ObjectProperty, StringProperty
from kivy.animation import Animation

from .shared import Page
from ..progress_elements import StatWidget
from ..forms import LogonForm
from ...utils.workers import Worker
from ...utils.jobs import AuthJobs
from ...utils.directives import include

include(__file__)

class Index(Page):
    __worker_events__ = 'on_status',

    animation = None
    name = 'index'
    anchor: StatWidget = ObjectProperty()

    def on_parent(self, *args):
        if args[1] is None:
            self.cancel_animation('offline')

    def on_status(self, **kwargs):
        status = kwargs['status']
        if status == 'connecting':
            return self.create_animation()
        self.cancel_animation(status)
        if status == 'online':
            self.root.connection_established()

    def create_animation(self):
        self.animation = anim = Animation(animation_angle=360, animation_cover_angle=-360, d=3)
        anim += Animation(animation_angle=0, animation_cover_angle=0, d=3)
        anchor = self.anchor
        anchor.ring_color = anchor.ring_colors[1]
        anchor.ring_cover_color = anchor.ring_colors[2]
        anchor.ring_trim, anchor.trim_extra = anchor.ring_trims
        anchor.ring_image = 'connecting'
        anim.repeat = True
        anim.start(anchor)

    def cancel_animation(self, stat_image: str):
        if animation := self.animation:
            self.animation = None
            anchor = self.anchor
            animation.cancel(anchor)
            anchor.opacity = 1
            anchor.ring_image = stat_image
            anchor.ring_color = anchor.ring_cover_color = anchor.ring_colors[0]
            anchor.ring_trim = anchor.trim_extra = 0
            anchor.animation_angle = anchor.animation_cover_angle = 0

class Logon(Page):
    __worker_events__ = 'on_signed_in',

    name = 'logon'
    form: LogonForm | None = ObjectProperty(allownone=True)

    def on_signed_in(self, **kwargs):
        user = kwargs.get('user')
        if user is None:
            self.form.post_submit(error=kwargs['message'], is_disabled=False)
        else:
            form = self.form
            self.form = None
            form.post_submit(is_disabled=True)
            self.root.signed_in(user)

    def on_submit(self):
        worker: Worker = self.app.worker
        creds = {'email': self.form.username.value, 'password': self.form.password.value}
        signin_job = AuthJobs.signin(creds)
        worker.post_job(**signin_job)

class WithProgElement(Page):
    def on_ids(self, *args):
        if 'prog_ele' in args[1]:
            self.ids.prog_ele.spin()

    def on_parent(self, *args):
        if args[1] is None:
            self.ids.prog_ele.halt()

class Welcome(WithProgElement):
    name = 'welcome'
    message = StringProperty('[size=48][i][b]Welcome[/b][/i][/size], [color=#70ffc9]{0}[/color]')

class Logout(WithProgElement):
    name = 'logout'
