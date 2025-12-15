from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior

# ---- needed imports for kv file ---

# noinspection PyUnusedImports
from components import PointedButton, CustomRecycleView


# ----


class ListLabel(RecycleDataViewBehavior, Label):
    pass


class EditWorldsDialog(BoxLayout):
    selected_dir = StringProperty(defaultvalue="")
    confirm = ObjectProperty()
    cancel = ObjectProperty()

    def __init__(self, **kwargs):
        super(EditWorldsDialog, self).__init__(**kwargs)
        dataList = [{'text': self.selected_dir}]
        dataList += [{'text': str(x)} for x in range(100)]
        self.ids.worldEditList.data = dataList
