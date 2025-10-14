from kivy_garden.hover import HoverBehavior
from kivy.uix.button import Button

import utils
import constants


class PointedButton(HoverBehavior, Button):
    def on_hover_enter(self, me):
        utils.set_cursor(constants.CURSOR_HAND)

    def on_hover_update(self, me):
        utils.set_cursor(constants.CURSOR_HAND)

    def on_hover_leave(self, me):
        utils.set_cursor(constants.CURSOR_ARROW)
