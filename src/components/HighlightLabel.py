from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy_garden.hover import HoverBehavior

import utils
from constants import CURSOR_HAND, CURSOR_ARROW


class HighlightLabel(HoverBehavior, Label):
    def __init__(self, **kwargs):
        super(HighlightLabel, self).__init__(**kwargs)
        self._instructions = []

    def on_hover_enter(self, me):
        utils.set_cursor(CURSOR_HAND)
        for uid, zones in self.refs.items():
            self._highlight_ref(uid)

    def on_hover_update(self, me):
        utils.set_cursor(CURSOR_HAND)

    def on_hover_leave(self, me):
        utils.set_cursor(CURSOR_ARROW)
        self._clear_instructions()

    def _highlight_ref(self, name):
        if self._instructions:
            return
        store = self._instructions.append
        with self.canvas:
            store(Color(0, 1, 0, 0.25))

        for box in self.refs[name]:
            box_x = self.center_x - self.texture_size[0] * 0.5 + box[0]
            box_y = self.center_y + self.texture_size[1] * 0.5 - box[1]
            box_w = box[2] - box[0]
            box_h = box[1] - box[3]
            with self.canvas:
                store(Rectangle(
                    pos=(box_x, box_y), size=(box_w, box_h)))

    def _clear_instructions(self):
        rm = self.canvas.remove
        for instr in self._instructions:
            rm(instr)
        self._instructions = []
