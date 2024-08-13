from kivy.app import App
from kivy.uix.image import Image
from kivy.core.window import Window


class ReactiveImage(Image):
    def __init__(self, **kwargs):
        super(ReactiveImage, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos_on_button)
        self._active = False

    def on_mouse_pos_on_button(self, *largs):
        pos = self.to_widget(*largs[1])
        if self.collide_point(*pos):
            self._reaction_ref()
            return
        if self._active:
            self._clear_instructions()

    def _reaction_ref(self):
        if self._active:
            return
        self._coreimage.anim_reset(True)
        self._active = True

    def _clear_instructions(self):
        if not self._active:
            return
        self._coreimage.anim_reset(True)
        self._coreimage.anim_reset(False)
        self._active = False


class TestApp(App):
    pass


TestApp().run()
