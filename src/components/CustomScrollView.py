from kivy.uix.scrollview import ScrollView
import constants


class CustomScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(CustomScrollView, self).__init__(
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=['bars', 'content'],
            scroll_wheel_distance=constants.DEFAULT_SCROLL_WHEEL_DISTANCE,
            bar_width=constants.DEFAULT_BAR_WIDTH,
            always_overscroll=False,
            **kwargs
        )
