from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty

# ---- needed imports for kv file ---

# noinspection PyUnusedImports
from components import PointedButton

# ----


class EditWorldsDialog(BoxLayout):
    selected_dir = StringProperty(defaultvalue="")
    confirm = ObjectProperty(None)
    cancel = ObjectProperty(None)
