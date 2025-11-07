from PySide6.QtCore import QObject, Signal
from pynput import mouse, keyboard

from ok import Logger, og

logger = Logger.get_logger(__name__)


class Globals(QObject):
    clicked = Signal(int, int, object, bool)
    pressed = Signal(object)

    def __init__(self, exit_event):
        super().__init__()
        self.pynput_mouse = None
        self.pynput_keyboard = None
        exit_event.bind_stop(self)
        self.init_pynput()

    def stop(self):
        logger.info("pynput stop")
        self.reset_pynput()

    def init_pynput(self):
        logger.info("pynput start")
        if self.pynput_mouse is None:
            self.pynput_mouse = mouse.Listener(on_click=self.on_click)
            self.pynput_mouse.start()
        if self.pynput_keyboard is None:
            self.pynput_keyboard = keyboard.Listener(on_press=self.on_press)
            self.pynput_keyboard.start()

    def reset_pynput(self):
        if self.pynput_mouse:
            self.pynput_mouse.stop()
            self.pynput_mouse = None
        if self.pynput_keyboard:
            self.pynput_keyboard.stop()
            self.pynput_keyboard = None

    def on_click(self, x, y, button, pressed):
        self.clicked.emit(x, y, button, pressed)
    
    def on_press(self, key):
        self.pressed.emit(key)
        


if __name__ == "__main__":
    glbs = Globals(exit_event=None)
