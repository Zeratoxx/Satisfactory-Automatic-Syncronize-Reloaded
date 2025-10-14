import kivy

kivy.require('2.3.0')

from kivy.config import Config
from constants import DEFAULT_WIDTH, DEFAULT_HEIGHT

Config.set('kivy', 'desktop', '1')
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'width', DEFAULT_WIDTH)
Config.set('graphics', 'height', DEFAULT_HEIGHT)
Config.set('graphics', 'minimum_width', DEFAULT_WIDTH)
Config.set('graphics', 'minimum_height', DEFAULT_HEIGHT)
# Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'position', 'auto')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
import os
import sys
from kivy.resources import resource_add_path
from kivy.uix.gridlayout import GridLayout

from kivy_garden.hover import HoverManager

from pages import Home


# ---- needed imports for kv file ---

# noinspection PyUnusedImports
from components.HighlightLabel import HighlightLabel

# ----


class SatisfactoryAutomaticSynchronizeReloaded(GridLayout):
    pass


class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hover_manager = HoverManager()

    def build(self):
        self.title = 'SASR - Satisfactory Automatic Synchronize Reloaded'
        self.icon = 'res/images/icons8-zufriedenstellend-256.png'
        root = SatisfactoryAutomaticSynchronizeReloaded()
        content = Home()
        root.add_widget(content)
        content.second_init()
        return root

    def on_start(self):
        super().on_start()
        self.root_window.register_event_manager(self.hover_manager)
        # self.root_window.clearcolor = (0.12, 0.12, 0.12, 1.0)

    def on_stop(self):
        super().on_stop()
        self.root_window.unregister_event_manager(self.hover_manager)


if __name__ == '__main__':
    kivy.require('2.3.0')
    if hasattr(sys, '_MEIPASS'):
        # noinspection PyProtectedMember
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()
