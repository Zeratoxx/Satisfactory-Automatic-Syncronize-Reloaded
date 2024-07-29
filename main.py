from tkinter import *
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget
)
import sys
from random import randint
from kivy.app import App
from kivy.uix.widget import Widget


class PongGame(Widget):
    pass


class PongApp(App):
    def build(self):
        return PongGame()


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class QtWindowFromTutorial(QWidget):

    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        Button1 = QPushButton('PyQt')
        Button2 = QPushButton('Layout')
        Button3 = QPushButton('Management')

        layout = QVBoxLayout()
        layout.addWidget(Button1)
        layout.addWidget(Button2)
        layout.addWidget(Button3)

        self.setLayout(layout)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('PyQt5 Layout')
        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = AnotherWindow()
        self.window2 = AnotherWindow()
        self.window3 = QtWindowFromTutorial()

        self.setWindowTitle("CodersLegacy")
        self.setGeometry(400, 400, 500, 300)

        l = QVBoxLayout()
        button1 = QPushButton("Push for Window 1")
        button1.clicked.connect(self.toggle_window1)
        l.addWidget(button1)

        button2 = QPushButton("Push for Window 2")
        button2.clicked.connect(self.toggle_window2)
        l.addWidget(button2)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def toggle_window1(self, checked):
        if self.window1.isVisible():
            self.window1.hide()

        else:
            self.window1.show()

    def toggle_window2(self, checked):
        if self.window2.isVisible():
            self.window2.hide()

        else:
            self.window2.show()

    def toggle_window3(self, checked):
        if self.window3.isVisible():
            self.window3.hide()

        else:
            self.window3.show()


def window_pyqt5():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


def window_tkinter():
    root = Tk()
    root.geometry("250x250")
    frame = Frame(root)
    frame.pack()

    leftframe = Frame(root)
    leftframe.pack(side=LEFT)

    rightframe = Frame(root)
    rightframe.pack(side=RIGHT)

    label = Label(frame, text="Hello world")
    label.pack()

    button1 = Button(leftframe, text="Button1")
    button1.pack(padx=3, pady=3)
    button2 = Button(rightframe, text="Button2")
    button2.pack(padx=3, pady=3)
    button3 = Button(leftframe, text="Button3")
    button3.pack(padx=3, pady=3)

    root.title("Test")
    root.mainloop()


def main():
    window_tkinter()
    window_pyqt5()
    PongApp().run()


if __name__ == '__main__':
    main()
