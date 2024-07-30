import kivy

kivy.require('2.3.0')

from kivy.config import Config

Config.set('kivy', 'desktop', '1')
Config.set('graphics', 'width', '560')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'minimum_width', '560')
Config.set('graphics', 'minimum_height', '600')
# Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'position', 'auto')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from src.libs.content.content import Content


class SatisfactoryAutomaticSynchronizeReloaded(GridLayout):
    pass


class MainApp(App):
    def build(self):
        self.title = 'SASR - Satisfactory Automatic Synchronize Reloaded'
        self.icon = 'res/icons/icons8-zufriedenstellend-256.png'
        root = SatisfactoryAutomaticSynchronizeReloaded()
        root.add_widget(Content())
        return root


if __name__ == '__main__':
    kivy.require('2.3.0')
    MainApp().run()
