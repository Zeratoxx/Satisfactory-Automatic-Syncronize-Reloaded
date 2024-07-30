from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<MyWidget>:
    id: my_root
    drives_list: drives_list
    file_chooser: file_chooser
    RecycleView:
        id: drives_list
        viewclass: 'SelectableLabel'
        SelectableRecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            multiselect: False
            touch_multiselect: False
    FileChooserListView:
        id: file_chooser
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            self.parent.parent.parent.drive_selection_changed(rv.data[index])
        else:
            print("selection removed for {0}".format(rv.data[index]))


class MyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)
        self.ids.drives_list.data = [{'text': x} for x in self.get_win_drives()]

    @staticmethod
    def get_win_drives():
        if platform == 'win':
            import win32api

            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]

            print("drives found: {0}".format(drives))
            print("type of var 'drives': {0}".format(type(drives)))
            return drives
        else:
            return []

    def drive_selection_changed(self, *args):
        print(args)
        selected_item = args[0]['text']
        self.file_chooser.path = selected_item


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()
