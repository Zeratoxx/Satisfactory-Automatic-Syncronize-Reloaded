from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

# ---- needed imports for kv file ---

# noinspection PyUnusedImports
from components import PointedButton

# ----


class DirSelectDialog(FloatLayout):
    select_dir = ObjectProperty(None)
    cancel = ObjectProperty(None)
