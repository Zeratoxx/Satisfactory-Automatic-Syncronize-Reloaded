import os
from plyer import filechooser

from kivy.uix.dropdown import DropDown
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.utils import rgba
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from src.libs.content.dialogs import EditWorldsDialog, DirSelectDialog


# class MainBoxes(GridLayout):
#
#     def __init__(self, **kwargs):
#         super(MainBoxes, self).__init__(**kwargs)
#         self.cols = 2
#         self.add_widget(Label(text='User Name'))
#         self.username = TextInput(multiline=False)
#         self.add_widget(self.username)
#         self.add_widget(Label(text='password'))
#         self.password = TextInput(password=True, multiline=False)
#         self.add_widget(self.password)


class CustomDropDown(DropDown):
    pass


class Content(BoxLayout):

    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        dropdown = CustomDropDown()

        self.world_editor_popup = Popup(title="Edit worlds", content=EditWorldsDialog(confirm=self.confirm_world_list,
                                                                                      cancel=self.dismiss_popup),
                                        size_hint=(0.9, 0.9), separator_color=rgba(229, 148, 69))

        # self.world_editor_popup.content.children[2].children[0].bind(on_release=self.switch_popup_content)
        self.world_editor_popup.content.children[2].children[0].bind(on_release=self.open_system_dir_chooser)

        self.dir_select_popup = Popup(title="Select directory",
                                      content=DirSelectDialog(select_dir=self.select_dir,
                                                              cancel=self.cancel_select_dir),
                                      size_hint=(0.9, 0.9), separator_color=rgba(229, 148, 69))
        self._popup = self.world_editor_popup

        main_button = Button(text='Choose World...', size_hint_y=None, size_hint_x=1.45, height=60)
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))

        # access the BoxLayout with the id "worldChoiceContainer" defined in content.kv and add main_button
        self.ids.worldChoiceContainer.add_widget(main_button)

    def second_init(self):
        edit_button = Button(text='Edit Worlds...', size_hint_y=None, size_hint_x=1.45, height=60)
        # TODO use edit icon instead of text
        self.ids.worldChoiceContainer.add_widget(edit_button)
        edit_button.bind(on_release=self.show_edit_worlds)

    def dismiss_popup(self):
        self._popup.dismiss()

    def open_popup(self):
        self._popup.open()

    def open_system_dir_chooser(self, widget=None):
        path = filechooser.choose_dir(title="Select a directory...")
        if path is not None:
            self.world_editor_popup.content.selected_dir = path[0]
        else:
            print("path empty")

    def switch_popup_content(self, widget=None):
        print("firing switch_popup_content")
        self.dismiss_popup()
        if self._popup == self.world_editor_popup:
            print("opt1")
            self._popup = self.dir_select_popup
        elif self._popup == self.dir_select_popup:
            print("opt2")
            self._popup = self.world_editor_popup
        else:
            print("nothing fitted somehow")
        print("open")
        self.open_popup()

    def show_edit_worlds(self, widget):
        self._popup = self.world_editor_popup
        self.open_popup()

    def show_dir_select(self, widget):
        self._popup = self.dir_select_popup
        self.open_popup()

    def select_dir(self, path, filename):
        if filename is not None and filename is list and filename.__len__ > 0:
            self.world_editor_popup.content.selected_dir = os.path.join(path, filename[0])
        else:
            print("filename not given")
            self.world_editor_popup.content.selected_dir = os.path.join(path)
        self.switch_popup_content()

    def cancel_select_dir(self):
        self.switch_popup_content()

    def confirm_world_list(self):
        # TODO save
        self.dismiss_popup()
