from kivy.properties import ColorProperty, StringProperty, NumericProperty, ListProperty
from kivy.utils import rgba
from kivy.uix.label import Label

from ..utils.directives import include

include(__file__)

class StatWidget(Label):
    animation_angle = NumericProperty(0)
    animation_cover_angle = NumericProperty(0)
    cover_color = ColorProperty(rgba('#0e1574ff'))

    ring_colors = (
        rgba('#00000000'),
        rgba('#a5ff00ff'),
        rgba('#26e8e880'),
    )
    ring_color = ColorProperty(ring_colors[0])
    ring_cover_color = ColorProperty(ring_colors[0])

    ring_image = StringProperty('offline')
    ring_image_color = ColorProperty(rgba('#e8e8e8ff'))

    trim_extra = NumericProperty(0)
    ring_trim = NumericProperty(0)
    ring_trims = ListProperty(['2dp', '12dp'])
