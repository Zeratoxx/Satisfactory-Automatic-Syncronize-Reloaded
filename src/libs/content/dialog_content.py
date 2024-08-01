from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty


class DirSelectDialog(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class EditWorldsDialog(FloatLayout):
    confirm = ObjectProperty(None)
    cancel = ObjectProperty(None)
