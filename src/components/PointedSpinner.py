from kivy.uix.spinner import Spinner, SpinnerOption

from . import PointedButton


class PointedSpinnerOption(SpinnerOption, PointedButton):
    pass


class PointedSpinner(Spinner, PointedButton):
    option_cls = PointedSpinnerOption
