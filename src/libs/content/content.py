import os

from kivy.core.window import Window
from kivy.uix.image import Image
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
from winioctlcon import F3_720_512

import src.libs.constants as constants
from src.libs.content.dialogs import EditWorldsDialog, DirSelectDialog
from src.libs.utils import utils


# class PointedButton(Button):
#     def __init__(self, **kwargs):
#         super(PointedButton, self).__init__(**kwargs)
#         Window.bind(mouse_pos=self.on_mouse_pos_on_button)
#
#     def on_mouse_pos_on_button(self, *largs):
#         pos = self.to_widget(*largs[1])
#         if self.collide_point(*pos):
#             utils.set_cursor(constants.CURSOR_HAND)
#             return
#         utils.set_cursor(constants.CURSOR_ARROW)


class ReactiveButton(Button):
    def __init__(self, **kwargs):
        super(ReactiveButton, self).__init__(**kwargs)
        self._active = False

    def on_mouse_pos_on_button(self, *largs):
        # super(ReactiveButton, self).on_mouse_pos_on_button(*largs)
        pos = self.to_widget(*largs[1])
        if self.collide_point(*pos):
            self._reaction_ref()
            return
        if self._active:
            self._clear_instructions()

    def _reaction_ref(self):
        if self._active:
            return
        for child in self.children:
            if isinstance(child, Image):
                child._coreimage.anim_reset(True)
                child.anim_delay = 1/24
        self._active = True

    def _clear_instructions(self):
        if not self._active:
            return
        for child in self.children:
            if isinstance(child, Image):
                # child._coreimage.anim_reset(True)
                # child.anim_delay = -1
                pass
        self._active = False


class CustomDropDown(DropDown):
    # def __init__(self, **kwargs):
    #     super(CustomDropDown, self).__init__(**kwargs)
    #     Window.bind(mouse_pos=self.on_mouse_pos_on_button)
    #
    # def on_mouse_pos_on_button(self, *largs):
    #     pos = self.to_widget(*largs[1])
    #     if self.collide_point(*pos):
    #         utils.set_cursor(constants.CURSOR_HAND)
    #         return
    #     utils.set_cursor(constants.CURSOR_ARROW)
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

        self.ids.dropdown_main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.ids.dropdown_main_button, 'text', x))

        # access the BoxLayout with the id "worldChoiceContainer" defined in content.kv and add main_button

    def second_init(self):
        self.ids.edit_gif._coreimage.anim_reset(False)
        self.ids.editWorldsListButton.bind(on_release=self.show_edit_worlds)

    def dismiss_popup(self):
        self._popup.dismiss()

    def open_popup(self):
        self._popup.open()

    def open_system_dir_chooser(self, widget=None):
        # TODO default path for other OS'es
        # TODO fix default path on Windows
        path = filechooser.choose_dir(title="Select a directory...",
                                      path=os.path.expandvars(constants.SATISFACTORY_SAVED_FOLDER_PATH))
        if path is not None and len(path) != 0:
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
