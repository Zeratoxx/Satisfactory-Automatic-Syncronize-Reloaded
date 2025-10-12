from kivy.core.window import Window


def set_cursor(cursor_name_string: str):
    print("Set window cursor: \"" + cursor_name_string + "\"")
    Window.set_system_cursor(cursor_name_string)
