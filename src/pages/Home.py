import os.path
from pathlib import Path

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
# from kivy.core.window import Window
from plyer import filechooser
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

from kivy_garden.hover import HoverBehavior

import constants as constants
from content import EditWorldsDialog, DirSelectDialog
import utils

# ---- needed imports for kv file ---

# noinspection PyUnusedImports
from components import PointedButton, PointedToggleButton, ReactiveButton, Tooltip


# ----


class ReactiveButtonWithToolTip(ReactiveButton):
    def __init__(self, **kwargs):
        super(ReactiveButtonWithToolTip, self).__init__(**kwargs)
        self.tooltip = Tooltip(text="Edit Worlds...")

    def on_hover_enter(self, me):
        super(ReactiveButtonWithToolTip, self).on_hover_enter(me)
        self.update_tooltip_pos(me)
        self.display_tooltip()

    def on_hover_leave(self, me):
        super(ReactiveButtonWithToolTip, self).on_hover_leave(me)
        self.close_tooltip()

    def on_hover_update(self, me):
        super(ReactiveButtonWithToolTip, self).on_hover_update(me)
        self.update_tooltip_pos(me)

    def update_tooltip_pos(self, me):
        self.tooltip.pos = (me.pos[0] - self.tooltip.texture_size[0] / 2.3,
                            me.pos[1] - self.tooltip.texture_size[1] * 3)

    def close_tooltip(self, *args):
        Window.remove_widget(self.tooltip)

    def display_tooltip(self, *args):
        Window.add_widget(self.tooltip)


class CustomDropDown(HoverBehavior, DropDown):
    def on_hover_enter(self, me):
        utils.set_cursor(constants.CURSOR_HAND)

    def on_hover_update(self, me):
        utils.set_cursor(constants.CURSOR_HAND)

    def on_hover_leave(self, me):
        utils.set_cursor(constants.CURSOR_ARROW)


class Home(BoxLayout):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        dropdown = CustomDropDown()

        self.world_editor_popup = Popup(title="Edit worlds", content=EditWorldsDialog(confirm=self.confirm_world_list,
                                                                                      cancel=self.dismiss_popup),
                                        size_hint=constants.POPUP_SIZE_HINT,
                                        separator_color=constants.POPUP_SEPARATOR_COLOR)

        self.world_editor_popup.content.children[2].children[0].bind(on_release=self.switch_popup_content)
        # self.world_editor_popup.content.children[2].children[0].bind(on_release=self.open_system_dir_chooser)

        default_path = os.path.expandvars(constants.SATISFACTORY_SAVED_FOLDER_PATH)
        parsed_default_path = str(Path(default_path).resolve())
        self.dir_select_popup = Popup(title="Select directory",
                                      content=DirSelectDialog(select_dir=self.select_dir,
                                                              cancel=self.cancel_select_dir,
                                                              default_path=parsed_default_path),
                                      size_hint=constants.POPUP_SIZE_HINT,
                                      separator_color=constants.POPUP_SEPARATOR_COLOR)

        self._popup = self.world_editor_popup

        self.ids.dropdown_main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(self.ids.dropdown_main_button, 'text', x))

        # access the BoxLayout with the id “worldChoiceContainer" defined in content.kv and add main_button

    def second_init(self):
        # noinspection PyProtectedMember
        self.ids.edit_gif._coreimage.anim_reset(False)
        self.ids.editWorldsListButton.bind(on_release=self.show_edit_worlds)

        self.dir_select_popup.content.ids.filechooser.layout.ids.scrollview.scroll_type = ['bars', 'content']
        self.dir_select_popup.content.ids.filechooser.layout.ids.scrollview.scroll_wheel_distance = 50
        self.dir_select_popup.content.ids.filechooser.layout.ids.scrollview.bar_width = constants.DEFAULT_BAR_WIDTH

        self.ids.console_log_scrollview.bar_width= constants.DEFAULT_BAR_WIDTH
        # self.ids.console_log.text = "Nothing happened yet.\nWaiting for launch."
        self.ids.console_log.text = ("Nothing happened yet.\nWaiting for launch.\n"
                                     "Cum spatii cadunt, omnes galluses carpseris teres, dexter capioes.\n"
                                     "Heu, castus hibrida!\n"
                                     "Nuclear vexatum iacere de mirabilis demissio, visum ventus!\n"
                                     "Clabulares accelerare, tanquam emeritis cacula.\n"
                                     "Tatas assimilant, tanquam flavum impositio.\n"
                                     "Est talis palus, cesaris.\n"
                                     "Cur brodium peregrinationes?\n"
                                     "Nunquam acquirere luba.\n"
                                     "Pol, devirginato!\n"
                                     "A falsis, coordinatae alter lamia.\n"
                                     "Hippotoxotas mori!\n"
                                     "Superbus, festus magisters diligenter locus de bi-color, lotus lapsus.\n"
                                     "Genetrixs mori in camerarius hamburgum!\n"
                                     "Pol, fatalis fraticinida!\n"
                                     "Mensas sunt luras de mirabilis bulla.\n"
                                     "Pol, mineralis!\n"
                                     "Ollas peregrinatione in tolosa!\n"
                                     "A falsis, clabulare domesticus abactus.\n"
                                     "Cum advena ridetis, omnes assimilatioes consumere emeritis, domesticus gemnaes.\n"
                                     "Ubi est superbus turpis?\n"
                                     "Fatalis, varius deuss nunquam talem de nobilis, flavum racana.\n"
                                     "Primus pars sapienter dignuss victrix est.\n"
                                     "Nunquam desiderium particula.\n"
                                     "Urbs cresceres, tanquam fatalis poeta.\n"
                                     "Est barbatus eleates, cesaris.\n"
                                     "Pol, exemplar!\n"
                                     "Candidatuss sunt tumultumques de festus detrius.\n"
                                     "Orgias persuadere in emeritis brigantium!\n"
                                     "Compaters congregabo!\n"
                                     "Ubi est camerarius exemplar?\n"
                                     "Sunt rationees magicae fatalis, germanus demolitionees.\n"
                                     "Heu, barbatus mons!\n"
                                     "Castus, festus fidess superbe examinare de alter, neuter ausus.\n"
                                     "Cur assimilatio peregrinatione?\n"
                                     "Velox, castus abnobas una imperium de mirabilis, dexter triticum.\n"
                                     "Rusticus luras ducunt ad hippotoxota.\n"
                                     "Ecce.\n"
                                     "Historia festus spatii est.\n"
                                     "Eheu, albus idoleum!\n"
                                     "Aonides de raptus vigil, tractare hibrida!\n"
                                     "Est brevis nutrix, cesaris.\n"
                                     "Calcarias peregrinationes, tanquam audax nuclear vexatum iacere.\n"
                                     "Advena de fortis rumor, amor pars!\n"
                                     "Peritus verpas ducunt ad brodium.\n"
                                     "Cur poeta experimentum?\n"
                                     "Pol, a bene indictio.\n"
                                     "Nunquam convertam musa.\n"
                                     "Accelerare aegre ducunt ad castus fides.\n"
                                     "Est bi-color fortis, cesaris.\n"
                                     "Lactas potus in oenipons!\n"
                                     "Pol, a bene detrius, grandis luba!\n"
                                     "Nixuss observare in noster cubiculum!\n"
                                     "Ubi est varius onus?\n"
                                     "Est grandis fermium, cesaris.\n"
                                     "A falsis, cacula magnum terror.\n"
                                     "Messis velox ducunt ad superbus classis.\n"
                                     "Clemens lumen aegre imperiums itineris tramitem est.")

    def dismiss_popup(self):
        self._popup.dismiss()

    def open_popup(self):
        self._popup.open()

    def open_system_dir_chooser(self, widget=None):
        # TODO default path for other OS'es
        # TODO fix default path on Windows
        default_path = os.path.expandvars(constants.SATISFACTORY_SAVED_FOLDER_PATH)
        parsed_default_path = str(Path(default_path).resolve())
        print("default_path: " + default_path)
        print("str(Path(default_path).resolve()): " + parsed_default_path)
        # print("default_path: " + default_path)
        path = filechooser.choose_dir(title="Select the directory which contains your world." + parsed_default_path,
                                      path=parsed_default_path
                                      )
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
