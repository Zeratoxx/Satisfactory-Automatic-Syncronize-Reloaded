from kivy.app import runTouchApp
from kivy.lang import Builder
runTouchApp(Builder.load_string('''
#:import win kivy.core.window.Window

GridLayout:
    cols: 4
    Button:
        text:  'arrow'
        on_release: win.set_system_cursor('arrow')
    Button:
        text:  'ibeam'
        on_release: win.set_system_cursor('ibeam')
    Button:
        text: 'wait'
        on_release: win.set_system_cursor('wait')
    Button:
        text: 'crosshair'
        on_release: win.set_system_cursor('crosshair')
    Button:
        text: 'wait_arrow'
        on_release: win.set_system_cursor('wait_arrow')
    Button:
        text: 'size_nwse'
        on_release: win.set_system_cursor('size_nwse')
    Button:
        text: 'size_nesw'
        on_release: win.set_system_cursor('size_nesw')
    Button:
        text: 'size_we'
        on_release: win.set_system_cursor('size_we')
    Button:
        text: 'size_ns'
        on_release: win.set_system_cursor('size_ns')
    Button:
        text: 'size_all'
        on_release: win.set_system_cursor('size_all')
    Button:
        text: 'hand'
        on_release: win.set_system_cursor('hand')
    Button:
        text: 'no'
        on_release: win.set_system_cursor('no')
'''))
