from kivy.properties import ColorProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.animation import Animation

from .layouts import Box
from .progress_elements import StatWidget
from .forms import LogonForm
from ..utils.workers import Worker
from ..utils.jobs import AuthJobs
from ..utils.directives import include

include(__file__)

class View(Widget):
    app = ObjectProperty(allownone=True)
    root = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)
        self.schedule_listeners_registration()

    def schedule_listeners_registration(self, timeout=0.):
        Clock.schedule_once(lambda _: self.register_listeners(), timeout)

    def register_listeners(self):
        if self.app is None:
            self.schedule_listeners_registration(timeout=1/4)
        elif hasattr(self, '__worker_events__'):
            worker: Worker = self.app.worker
            for event_uid in self.__worker_events__:
                event_handler = getattr(self, event_uid)
                callback = lambda *_, **kwargs: event_handler(**kwargs)
                worker.fbind(event_uid, callback)

class Page(View, Screen):
    ...

class IndexPage(Page):
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

class LogonPage(Page, Screen):
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

class PagesManager(ScreenManager):
    root: View = ObjectProperty()

    def forget_and_switch(self, page: str | Page):
        if isinstance(page, str):
            page = self.get_new_page(page)
        forgotten_page = self.current_screen
        self.switch_to(page)
        self.remove_widget(forgotten_page)

    def get_new_page(self, name: str) -> Page:
        kwargs = {'root': self.root, 'app': self.root.app}
        if name == 'index':
            return IndexPage(**kwargs)
        elif name == 'logon':
            return LogonPage(**kwargs)
        elif name == 'welcome':
            return Page(name='welcome', **kwargs)

class Dashboard(View, Box):
    __worker_events__ = (
        'on_signed_out',
        'on_response',
    )
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
