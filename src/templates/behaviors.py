from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window

class Hovering(Widget):
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_hover')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(Hovering, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        obj_pos = args[1]
        entered = self.collide_point(*self.to_widget(*obj_pos))

        if self.hovered == entered:
            return
        self.hovered = entered
        self.dispatch('on_hover' if entered else 'on_leave')

    def on_hover(self):
        ...

    def on_leave(self):
        ...

class Clicking(Widget):
    __events__ = 'on_view', 'on_press', 'on_release',

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.disabled:
            if touch.is_double_tap:
                self.dispatch('on_view')
            else:
                self.dispatch('on_press')
            return True
        return super(Clicking, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and not self.disabled:
            self.dispatch('on_release')
            return True
        return super(Clicking, self).on_touch_up(touch)

    def on_view(self):
        ...

    def on_press(self):
        ...

    def on_release(self):
        ...
