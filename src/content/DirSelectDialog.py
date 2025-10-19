import os.path
from pathlib import Path

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

# ---- needed imports for kv file ---

# noinspection PyUnusedImports
from components import PointedButton


# ----


class DirSelectDialog(FloatLayout):
    def __init__(self, select_dir=ObjectProperty(), cancel=ObjectProperty(), default_path: str = None, **kwargs):
        super(DirSelectDialog, self).__init__(**kwargs)
        self.select_dir = select_dir
        self.cancel = cancel

        if default_path:
            expanded_path = os.path.expandvars(default_path)
            parsed_default_path = str(Path(expanded_path).resolve())
            self.ids.filechooser.path = parsed_default_path

        self.ids.filechooser.bind(on_entries_cleared=self.update_current_dir_label)
        self.update_current_dir_label()

    def update_current_dir_label(self, *largs):
        self.ids.current_path.text = self.ids.filechooser.path
