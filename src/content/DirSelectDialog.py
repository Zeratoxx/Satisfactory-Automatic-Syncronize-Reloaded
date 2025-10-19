import sys
import os.path
from pathlib import Path

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.stacklayout import StackLayout

# ---- needed imports for kv file ---

# noinspection PyUnusedImports
from components import PointedButton


# ----


class LocationSelectionButton(PointedButton):
    def __init__(self, **kwargs):
        super(LocationSelectionButton, self).__init__(**kwargs)
        self.size_hint_x = .166666666
        self.size_hint_y = None
        self.height = 40


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

        if sys.platform == 'win32':
            import win32api

            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            print(drives)
            for drive in drives:
                button = LocationSelectionButton(text=drive)
                button.bind(on_release=self.change_drive)
                self.ids.location_selector.add_widget(button)

    def update_current_dir_label(self, *largs):
        self.ids.current_path.text = self.ids.filechooser.path

    def change_drive(self, callback):
        self.ids.filechooser.path = str(
            Path(os.path.expandvars(callback if isinstance(callback, str) else callback.text)).resolve())
