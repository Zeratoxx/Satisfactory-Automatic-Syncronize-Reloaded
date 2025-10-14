from kivy.uix.image import Image

from . import PointedButton


class ReactiveButton(PointedButton):
    def __init__(self, **kwargs):
        super(ReactiveButton, self).__init__(**kwargs)

    def on_hover_enter(self, me):
        super(ReactiveButton, self).on_hover_enter(me)
        self._reaction_ref()

    def _reaction_ref(self):
        for child in self.children:
            if isinstance(child, Image):
                child._coreimage.anim_reset(True)
                child.anim_delay = 1 / 24
