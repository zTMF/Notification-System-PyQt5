import time

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget, QMainWindow

from messages.message_widget import MessageWidget


class MessageThread(QThread):
    add_signal: pyqtSignal = pyqtSignal(MessageWidget)

    def __init__(self, message: MessageWidget, parent: QWidget | QObject = None):
        super(MessageThread, self).__init__(parent)
        self.__message: MessageWidget = message

    @property
    def message(self) -> MessageWidget:
        return self.__message

    def run(self) -> None:
        time.sleep(1)
        self.add_signal.emit(self.__message)
