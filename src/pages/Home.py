import os.path
from pathlib import Path

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
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
from components import PointedButton, PointedToggleButton, ReactiveButton, ReactiveButtonWithToolTip, CustomScrollView


# ----


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
        self.dir_select_popup.content.ids.filechooser.layout.ids.scrollview.scroll_wheel_distance = (
            constants.DEFAULT_SCROLL_WHEEL_DISTANCE)
        self.dir_select_popup.content.ids.filechooser.layout.ids.scrollview.bar_width = constants.DEFAULT_BAR_WIDTH

        # self.ids.console_log.text = "Nothing happened yet.\nWaiting for launch."
        self.ids.console_log.text = (
            "Nothing happened yet.\nWaiting for launch.\nCum spatii cadunt, omnes galluses carpseris teres, dexter capioes.\nHeu, castus hibrida!\nNuclear vexatum iacere de mirabilis demissio, visum ventus!\nClabulares accelerare, tanquam emeritis cacula.\nTatas assimilant, tanquam flavum impositio.\nEst talis palus, cesaris.\nCur brodium peregrinationes?\nNunquam acquirere luba.\nPol, devirginato!\nA falsis, coordinatae alter lamia.\nHippotoxotas mori!\nSuperbus, festus magisters diligenter locus de bi-color, lotus lapsus.\nGenetrixs mori in camerarius hamburgum!\nPol, fatalis fraticinida!\nMensas sunt luras de mirabilis bulla.\nPol, mineralis!\nOllas peregrinatione in tolosa!\nA falsis, clabulare domesticus abactus.\nCum advena ridetis, omnes assimilatioes consumere emeritis, domesticus gemnaes.\nUbi est superbus turpis?\nFatalis, varius deuss nunquam talem de nobilis, flavum racana.\nPrimus pars sapienter dignuss victrix est.\nNunquam desiderium particula.\nUrbs cresceres, tanquam fatalis poeta.\nEst barbatus eleates, cesaris.\nPol, exemplar!\nCandidatuss sunt tumultumques de festus detrius.\nOrgias persuadere in emeritis brigantium!\nCompaters congregabo!\nUbi est camerarius exemplar?\nSunt rationees magicae fatalis, germanus demolitionees.\nHeu, barbatus mons!\nCastus, festus fidess superbe examinare de alter, neuter ausus.\nCur assimilatio peregrinatione?\nVelox, castus abnobas una imperium de mirabilis, dexter triticum.\nRusticus luras ducunt ad hippotoxota.\nEcce.\nHistoria festus spatii est.\nEheu, albus idoleum!\nAonides de raptus vigil, tractare hibrida!\nEst brevis nutrix, cesaris.\nCalcarias peregrinationes, tanquam audax nuclear vexatum iacere.\nAdvena de fortis rumor, amor pars!\nPeritus verpas ducunt ad brodium.\nCur poeta experimentum?\nPol, a bene indictio.\nNunquam convertam musa.\nAccelerare aegre ducunt ad castus fides.\nEst bi-color fortis, cesaris.\nLactas potus in oenipons!\nPol, a bene detrius, grandis luba!\nNixuss observare in noster cubiculum!\nUbi est varius onus?\nEst grandis fermium, cesaris.\nA falsis, cacula magnum terror.\nMessis velox ducunt ad superbus classis.\nClemens lumen aegre imperiums itineris tramitem est.")

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

    def select_dir(self, path, selectionList):
        if selectionList is not None and isinstance(selectionList, list) and len(selectionList) > 0:
            self.world_editor_popup.content.selected_dir = str(Path(selectionList[0]).resolve())
        else:
            print("Empty selection list")
            self.world_editor_popup.content.selected_dir = str(Path(path))
        self.switch_popup_content()

    def cancel_select_dir(self):
        self.switch_popup_content()

    def confirm_world_list(self):
        # TODO save
        self.dismiss_popup()
