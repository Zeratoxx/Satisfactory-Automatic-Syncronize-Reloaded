import kivy
from kivy.config import Config

Config.set('graphics', 'minimum_width', '500')
Config.set('graphics', 'minimum_height', '400')
from kivy.app import App

from src.interface.interface import Interface


class SatisfactoryAutomaticSynchronizeReloadedApp(App):

    def build(self):
        self.title = 'Satisfactory Automatic Synchronize Reloaded'
        self.icon = 'icons8-zufriedenstellend-256.png'
        return


if __name__ == '__main__':
    kivy.require('2.3.0')
    SatisfactoryAutomaticSynchronizeReloadedApp().run()
