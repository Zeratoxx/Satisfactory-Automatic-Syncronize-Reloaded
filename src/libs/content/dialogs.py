from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty


class DirSelectDialog(FloatLayout):
    select_dir = ObjectProperty(None)
    cancel = ObjectProperty(None)


class EditWorldsDialog(BoxLayout):
    selected_dir = StringProperty(defaultvalue="")
    confirm = ObjectProperty(None)
    cancel = ObjectProperty(None)
