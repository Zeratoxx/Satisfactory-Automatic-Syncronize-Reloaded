import kivy
from kivy.factory import Factory

from src.libs.content.dir_chooser_popup import DirSelectDialog

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
import os
import sys
from kivy.resources import resource_add_path
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from src.libs.content.content import Content


class SatisfactoryAutomaticSynchronizeReloaded(GridLayout):
    select_dir = ObjectProperty(None)
    world_editor_popup_content = ObjectProperty(None) #evtl nicht nötig

    def dismiss_popup(self):
        self._popup = Popup(title="Edit worlds", content=self.world_editor_popup_content,
                            size_hint=(0.9, 0.9))

    def show_select(self, widget):
        dir_select_dialog_content = DirSelectDialog(select=self.select, cancel=self.dismiss_popup)
        self._popup = Popup(title="Select directory", content=dir_select_dialog_content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def select(self, path, filename):
        self.select_dir.text = os.path.join(path, filename[0])
        self.dismiss_popup()
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
