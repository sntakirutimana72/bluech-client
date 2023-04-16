from kivy.properties import ColorProperty, StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.utils import rgba
from kivy.animation import Animation

from .behaviors.layouts import BLayout
from .progress_elements import StatWidget
from ..utils.workers import Worker
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
            for event in self.__worker_events__:
                handler = getattr(self, event)
                worker.fbind(event, handler)

class Page(View, Screen):
    ...

class IndexPage(Page):
    __events__ = 'on_status',
    __worker_events__ = __events__

    animation = None
    name = 'index'

    animation_anchor: StatWidget = ObjectProperty()

    def on_parent(self, _, parent):
        if parent is None:
            self.cancel_animation('offline')

    def on_status(self, *_, **kwargs):
        stat_label = kwargs['status']
        if stat_label == 'connecting':
            return self.create_animation()
        self.cancel_animation(stat_label)
        if stat_label == 'online':
            self.root.on_connection_established()

    def create_animation(self):
        self.animation = anim = Animation(animation_angle=360, animation_cover_angle=-360, duration=3)
        anim += Animation(animation_angle=0, animation_cover_angle=0, duration=3)
        anchor = self.animation_anchor
        anchor.ring_color = anchor.ring_colors[1]
        anchor.ring_cover_color = anchor.ring_colors[2]
        anchor.ring_trim, anchor.trim_extra = anchor.ring_trims
        anchor.ring_image = 'connecting'
        anim.repeat = True
        anim.start(anchor)

    def cancel_animation(self, stat_image: str):
        if animation := self.animation:
            self.animation = None
            anchor = self.animation_anchor
            animation.cancel(anchor)
            anchor.opacity = 1
            anchor.ring_image = stat_image
            anchor.ring_color = anchor.ring_cover_color = anchor.ring_colors[0]
            anchor.ring_trim = anchor.trim_extra = 0
            anchor.animation_angle = anchor.animation_cover_angle = 0

class LogonPage(Page, Screen):
    name = 'logon'

    title = StringProperty('Logon')

class PagesManager(ScreenManager):
    root: View = ObjectProperty()

    def forget_and_switch_page(self, page: str | Page):
        if isinstance(page, str):
            page = self.get_new_page(page)
        forgotten_page = self.current_screen
        self.switch_to(page)
        self.remove_widget(forgotten_page)

    def get_new_page(self, name: str) -> Page:
        kwargs = {
            'root': self.root,
            'app': self.root.app
        }
        if name == 'index':
            return IndexPage(**kwargs)
        elif name == 'logon':
            return LogonPage(**kwargs)

class Dashboard(View, BLayout):
    __events__ = (
        'on_signed_in',
        'on_signed_out',
        'on_response',
    )
    __worker_events__ = __events__

    background_color = ColorProperty(rgba('#0e1574ff'))
    manager: PagesManager = ObjectProperty()

    def on_connection_established(self):
        self.manager.forget_and_switch_page('logon')

    def on_signed_in(self, **kwargs):
        ...

    def on_signed_out(self, **kwargs):
        self.manager.forget_and_switch_page('index')

    def on_response(self, **kwargs):
        ...