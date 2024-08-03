import kivy
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

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


class DirSelectDialog(FloatLayout):
    select_dir = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    pass


class DirSelect(App):
    pass


if __name__ == '__main__':
    DirSelect().run()
