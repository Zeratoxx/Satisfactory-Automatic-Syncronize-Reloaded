from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label

# ---- needed imports for kv file ---

# noinspection PyUnusedImports
from components import PointedButton, CustomScrollView

# ----


class ListLabel(Label):
    pass


class EditWorldsDialog(BoxLayout):
    selected_dir = StringProperty(defaultvalue="")
    confirm = ObjectProperty()
    cancel = ObjectProperty()

    def __init__(self, **kwargs):
        super(EditWorldsDialog, self).__init__(**kwargs)
        self.ids.worldEditList.bind(minimum_height=self.ids.worldEditList.setter('height'))
