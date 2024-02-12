from kivy.properties import (
    NumericProperty, StringProperty, ColorProperty, ListProperty,
    ObjectProperty, BooleanProperty,
)
from kivy.uix.boxlayout import BoxLayout

from ..utils.directives import include

include(__file__)

class TextField(BoxLayout):
    __events__ = 'on_change', 'on_blur',

    observables = None

    font_size = NumericProperty('14sp')
    font_name = StringProperty('Roboto')
    font_color = ColorProperty('black')

    cursor_color = ColorProperty('black')
    name = StringProperty('')

    placeholder = StringProperty('Enter here')
    placeholder_color = ColorProperty('#12122080')

    border = NumericProperty('1sp')
    border_blur = NumericProperty('2sp')
    border_radius = ListProperty([4, 4, 4, 4])
    border_color = ColorProperty('blue')
    border_blur_color = ColorProperty('green')
    background_color = ColorProperty('#e8e8e8cc')

    prompt = ObjectProperty()

    def on_change(self, new_val: str):
        ...

    def on_blur(self, new_val: bool):
        # Swap border colors on blur
        blur_bcolor = self.border_blur_color
        self.border_blur_color = self.border_color
        self.border_color = blur_bcolor
        # Swap border width
        blur_border = self.border_blur
        self.border_blur = self.border
        self.border = blur_border

    def on_text_change(self, new_value: str):
        self.dispatch('on_change', new_value)

    def on_focus_change(self, new_focus: bool):
        self.dispatch('on_blur', new_focus)

    def on_prompt(self, *args):
        instance = args[1]

        if instance and self.observables:
            for attrib in self.observables:
                if hasattr(self, attrib) and hasattr(instance, attrib):
                    attrib_val = getattr(self, attrib)
                    setattr(instance, attrib, attrib_val)

    @property
    def value(self) -> str:
        return self.prompt.text

    @value.setter
    def value(self, new_value: str):
        self.prompt.text = new_value

class TextAreaField(TextField):
    observables = ('multiline',)

    multiline = BooleanProperty(True)
