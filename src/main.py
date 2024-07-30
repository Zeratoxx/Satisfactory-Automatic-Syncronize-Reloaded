import kivy

kivy.require('2.3.0')

from kivy.config import Config

default_width = '560'
default_height = '600'
Config.set('kivy', 'desktop', '1')
Config.set('graphics', 'width', default_width)
Config.set('graphics', 'height', default_height)
Config.set('graphics', 'minimum_width', default_width)
Config.set('graphics', 'minimum_height', default_height)
# Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'position', 'auto')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import os
import sys
from kivy.resources import resource_add_path

from src.libs.content.content import Content


class SatisfactoryAutomaticSynchronizeReloaded(GridLayout):
    pass


class MainApp(App):
    def build(self):
        self.title = 'SASR - Satisfactory Automatic Synchronize Reloaded'
        self.icon = 'res/images/icons8-zufriedenstellend-256.png'
        root = SatisfactoryAutomaticSynchronizeReloaded()
        root.add_widget(Content())
        return root


if __name__ == '__main__':
    kivy.require('2.3.0')
    if hasattr(sys, '_MEIPASS'):
        # noinspection PyProtectedMember
        resource_add_path(os.path.join(sys._MEIPASS))
    MainApp().run()
