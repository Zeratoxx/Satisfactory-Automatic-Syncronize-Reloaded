from kivy.uix.recycleview import RecycleView
from . import CustomScrollView


class CustomRecycleView(RecycleView, CustomScrollView):
    def __init__(self, **kwargs):
        super(CustomRecycleView, self).__init__(**kwargs)
