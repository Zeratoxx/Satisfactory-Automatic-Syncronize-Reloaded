import kivy

kivy.require('2.3.0')

from kivy.config import Config

default_width = '560'
default_height = '600'
Config.set('kivy', 'desktop', '1')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'width', default_width)
Config.set('graphics', 'height', default_height)
Config.set('graphics', 'minimum_width', default_width)
Config.set('graphics', 'minimum_height', default_height)
# Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'position', 'auto')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
import os
import sys
from kivy.resources import resource_add_path
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label

from src.libs.content.content import Content


class HighlightLabel(Label):
    def __init__(self, **kwargs):
        super(HighlightLabel, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self._instructions = []

    def on_mouse_pos(self, *largs):
        pos = self.to_widget(*largs[1])
        if self.collide_point(*pos):
            tx, ty = pos
            tx -= self.center_x - self.texture_size[0] / 2.
            ty -= self.center_y - self.texture_size[1] / 2.
            ty = self.texture_size[1] - ty
            for uid, zones in self.refs.items():
                for zone in zones:
                    x, y, w, h = zone
                    if x <= tx <= w and y <= ty <= h:
                        self._highlight_ref(uid)
                        return
        if self._instructions:
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


class SatisfactoryAutomaticSynchronizeReloaded(GridLayout):
    pass


class MainApp(App):
    def build(self):
        self.title = 'SASR - Satisfactory Automatic Synchronize Reloaded'
        self.icon = 'res/images/icons8-zufriedenstellend-256.png'
        root = SatisfactoryAutomaticSynchronizeReloaded()
        content = Content()
        root.add_widget(content)
        content.second_init()
        return root


if __name__ == '__main__':
    kivy.require('2.3.0')
    if hasattr(sys, '_MEIPASS'):
        # noinspection PyProtectedMember
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()
