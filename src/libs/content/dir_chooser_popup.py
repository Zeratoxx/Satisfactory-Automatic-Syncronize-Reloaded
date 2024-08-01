from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import os


class DirSelectDialog(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)

