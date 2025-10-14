from kivy.uix.togglebutton import ToggleButton
from kivy_garden.hover import HoverBehavior

import constants
import utils


class PointedToggleButton(HoverBehavior, ToggleButton):
    def on_hover_enter(self, me):
        utils.set_cursor(constants.CURSOR_HAND)

    def on_hover_update(self, me):
        utils.set_cursor(constants.CURSOR_HAND)

    def on_hover_leave(self, me):
        utils.set_cursor(constants.CURSOR_ARROW)
