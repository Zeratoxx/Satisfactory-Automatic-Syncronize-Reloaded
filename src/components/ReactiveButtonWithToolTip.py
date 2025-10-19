from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.label import Label

from . import ReactiveButton

Builder.load_string('''
<Tooltip>:
    size_hint: None, None
    size: self.texture_size[0]+5, self.texture_size[1]+5
    canvas.before:
        Color:
            rgb: 0.2, 0.2, 0.2
        Rectangle:
            size: self.size
            pos: self.pos
''')


class Tooltip(Label):
    pass


class ReactiveButtonWithToolTip(ReactiveButton):
    tooltip_text = StringProperty()

    def __init__(self, **kwargs):
        super(ReactiveButtonWithToolTip, self).__init__(**kwargs)
        self.tooltip = Tooltip()

    def on_hover_enter(self, me):
        super(ReactiveButtonWithToolTip, self).on_hover_enter(me)
        if self.tooltip.text != self.tooltip_text:
            self.tooltip.text = self.tooltip_text
        self.update_tooltip_pos(me)
        self.display_tooltip()

    def on_hover_leave(self, me):
        super(ReactiveButtonWithToolTip, self).on_hover_leave(me)
        self.close_tooltip()

    def on_hover_update(self, me):
        super(ReactiveButtonWithToolTip, self).on_hover_update(me)
        self.update_tooltip_pos(me)

    def update_tooltip_pos(self, me):
        self.tooltip.pos = (me.pos[0] - self.tooltip.texture_size[0] / 2.3,
                            me.pos[1] - self.tooltip.texture_size[1] * 3)

    def close_tooltip(self):
        Window.remove_widget(self.tooltip)

    def display_tooltip(self):
        Window.add_widget(self.tooltip)
