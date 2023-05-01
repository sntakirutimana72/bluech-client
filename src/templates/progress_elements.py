from kivy.properties import ColorProperty, StringProperty, NumericProperty, ListProperty
from kivy.utils import rgba
from kivy.uix.widget import Widget
from kivy.animation import Animation

from ..utils.directives import include

include(__file__)

class StatWidget(Widget):
    animation_angle = NumericProperty(0)
    animation_cover_angle = NumericProperty(0)
    cover_color = ColorProperty('#0e1574ff')

    ring_colors = (
        rgba('#00000000'),
        rgba('#a5ff00ff'),
        rgba('#26e8e880'),
    )
    ring_color = ColorProperty(ring_colors[0])
    ring_cover_color = ColorProperty(ring_colors[0])

    ring_image = StringProperty('offline')
    ring_image_color = ColorProperty('#e8e8e8ff')

    trim_extra = NumericProperty(0)
    ring_trim = NumericProperty(0)
    ring_trims = ListProperty(['2dp', '12dp'])

class RingSpin(Widget):
    ring_color = ColorProperty('gray')
    angle = NumericProperty(0)
    cover_color = ColorProperty('#40ff88ff')

    animation = None

    def halt(self):
        if anim := self.animation:
            self.animation = None
            anim.cancel(self)

    def spin(self):
        self.animation = anim = Animation(angle=360, duration=1.75)
        anim += Animation(angle=0, duration=-1)
        anim.start(self)
