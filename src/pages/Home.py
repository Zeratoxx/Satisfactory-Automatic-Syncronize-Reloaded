import os.path
from pathlib import Path

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

import constants as constants
from content import EditWorldsDialog, DirSelectDialog

# ---- needed imports for kv file ---

# noinspection PyUnusedImports
from components import PointedButton, PointedToggleButton, ReactiveButton, ReactiveButtonWithToolTip, \
    CustomScrollView, PointedSpinner


# ----


class Home(BoxLayout):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)

        self.world_editor_popup = self.__get_world_editor_popup__()
        self.dir_select_popup = self.__get_dir_select_popup__()
        self._popup = self.world_editor_popup

        # TODO access the BoxLayout with the id “worldChoiceContainer" defined in content.kv and add main_button

    def second_init(self):
        self.ids.content_wrapper.size_hint_max_x = constants.INNER_MAX_WIDTH

        # noinspection PyProtectedMember
        self.ids.edit_gif._coreimage.anim_reset(False)
        self.ids.editWorldsListButton.bind(on_release=self.show_edit_worlds)
        self.ids.world_chooser_spinner.values = ['My first Item', 'My first and half Item', 'My second Item']  # TODO replace with dynamic world list
        self.ids.console_log.text = "Nothing happened yet.\nWaiting for launch."
        # self.ids.console_log.text = ("Nothing happened yet.\nWaiting for launch.\nCum spatii cadunt, omnes galluses carpseris teres, dexter capioes.\nHeu, castus hibrida!\nNuclear vexatum iacere de mirabilis demissio, visum ventus!\nClabulares accelerare, tanquam emeritis cacula.\nTatas assimilant, tanquam flavum impositio.\nEst talis palus, cesaris.\nCur brodium peregrinationes?\nNunquam acquirere luba.\nPol, devirginato!\nA falsis, coordinatae alter lamia.\nHippotoxotas mori!\nSuperbus, festus magisters diligenter locus de bi-color, lotus lapsus.\nGenetrixs mori in camerarius hamburgum!\nPol, fatalis fraticinida!\nMensas sunt luras de mirabilis bulla.\nPol, mineralis!\nOllas peregrinatione in tolosa!\nA falsis, clabulare domesticus abactus.\nCum advena ridetis, omnes assimilatioes consumere emeritis, domesticus gemnaes.\nUbi est superbus turpis?\nFatalis, varius deuss nunquam talem de nobilis, flavum racana.\nPrimus pars sapienter dignuss victrix est.\nNunquam desiderium particula.\nUrbs cresceres, tanquam fatalis poeta.\nEst barbatus eleates, cesaris.\nPol, exemplar!\nCandidatuss sunt tumultumques de festus detrius.\nOrgias persuadere in emeritis brigantium!\nCompaters congregabo!\nUbi est camerarius exemplar?\nSunt rationees magicae fatalis, germanus demolitionees.\nHeu, barbatus mons!\nCastus, festus fidess superbe examinare de alter, neuter ausus.\nCur assimilatio peregrinatione?\nVelox, castus abnobas una imperium de mirabilis, dexter triticum.\nRusticus luras ducunt ad hippotoxota.\nEcce.\nHistoria festus spatii est.\nEheu, albus idoleum!\nAonides de raptus vigil, tractare hibrida!\nEst brevis nutrix, cesaris.\nCalcarias peregrinationes, tanquam audax nuclear vexatum iacere.\nAdvena de fortis rumor, amor pars!\nPeritus verpas ducunt ad brodium.\nCur poeta experimentum?\nPol, a bene indictio.\nNunquam convertam musa.\nAccelerare aegre ducunt ad castus fides.\nEst bi-color fortis, cesaris.\nLactas potus in oenipons!\nPol, a bene detrius, grandis luba!\nNixuss observare in noster cubiculum!\nUbi est varius onus?\nEst grandis fermium, cesaris.\nA falsis, cacula magnum terror.\nMessis velox ducunt ad superbus classis.\nClemens lumen aegre imperiums itineris tramitem est.")  # TODO delete

    def __get_world_editor_popup__(self):
        world_editor_popup = Popup(title="Edit worlds", content=EditWorldsDialog(confirm=self.confirm_world_list,
                                                                                 cancel=self.dismiss_popup),
                                   size_hint=constants.POPUP_SIZE_HINT,
                                   size_hint_max_x=constants.INNER_MAX_WIDTH + 50,
                                   separator_color=constants.POPUP_SEPARATOR_COLOR)
        world_editor_popup.content.ids.addWorldButton.bind(on_release=self.switch_popup_content)
        return world_editor_popup

    def __get_dir_select_popup__(self):
        default_path = os.path.expandvars(constants.SATISFACTORY_SAVED_FOLDER_PATH)
        parsed_default_path = str(Path(default_path).resolve())
        dir_select_popup = Popup(title="Select directory",
                                 content=DirSelectDialog(select_dir=self.select_dir,
                                                         cancel=self.cancel_select_dir,
                                                         default_path=parsed_default_path),
                                 size_hint=constants.POPUP_SIZE_HINT,
                                 size_hint_max_x=constants.INNER_MAX_WIDTH + 50,
                                 separator_color=constants.POPUP_SEPARATOR_COLOR)
        dir_select_popup.content.ids.filechooser.layout.ids.scrollview.scroll_type = ['bars', 'content']
        dir_select_popup.content.ids.filechooser.layout.ids.scrollview.scroll_wheel_distance = (
            constants.DEFAULT_SCROLL_WHEEL_DISTANCE)
        dir_select_popup.content.ids.filechooser.layout.ids.scrollview.bar_width = constants.DEFAULT_BAR_WIDTH
        return dir_select_popup

    def dismiss_popup(self):
        self._popup.dismiss()

    def open_popup(self):
        self._popup.open()

    def switch_popup_content(self, widget=None):
        print("firing switch_popup_content")  # TODO remove
        self.dismiss_popup()
        if self._popup == self.world_editor_popup:
            print("opt1")  # TODO remove
            self._popup = self.dir_select_popup
        elif self._popup == self.dir_select_popup:
            print("opt2")  # TODO remove
            self._popup = self.world_editor_popup
        else:
            print("nothing fitted somehow")  # TODO remove
        print("open")  # TODO remove
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
            print("Empty selection list")  # TODO remove
            self.world_editor_popup.content.selected_dir = str(Path(path))
        self.switch_popup_content()

    def cancel_select_dir(self):
        self.switch_popup_content()

    def confirm_world_list(self):
        # TODO save
        self.dismiss_popup()
