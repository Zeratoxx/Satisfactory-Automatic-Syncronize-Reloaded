from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class CustomDropDown(DropDown):
    pass


class MainBoxes(GridLayout):

    def __init__(self, **kwargs):
        super(MainBoxes, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


class Content(BoxLayout):
    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        dropdown = CustomDropDown()

        main_button = Button(text='Choose World...', size_hint_y=None, size_hint_x=1.45, height=60)
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))

        # access the BoxLayout with the id "worldChoiceContainer" defined in content.kv and add main_button
        self.ids.worldChoiceContainer.add_widget(main_button)
