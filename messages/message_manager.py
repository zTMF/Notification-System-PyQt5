import random
from queue import Queue
from threading import Lock, Semaphore

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QEasingCurve, QTimer
from PyQt5.QtWidgets import QWidget

from messages.message_thread import MessageThread
from messages.message_widget import MessageWidget


class MessageManager(QObject):
    thread_count_changed: pyqtSignal = pyqtSignal(int)

    def __init__(self, parent: QWidget = None):
        super(MessageManager, self).__init__(parent)
        self.__message_list: list = []
        self.__thread_wait_list: list = []
        self.__limit: int = 4
        self.__count: int = 0
        self.__offset: int = 50
        self.__remove_flag: bool = False
        self.__animation_by_combo_box: QEasingCurve = QEasingCurve.OutBack
        self.__duration_by_combo_box: float = 0.5

    def __clean_all(self) -> None:
        self.__remove_flag = True
        # Messages Running
        for message in self.__message_list:
            message.disconnect()
            message.force_close_animation()
        self.__message_list.clear()

        # In Threading Messages
        for message in self.__thread_wait_list:
            message.message.deleteLater()
            message.terminate()
            message.deleteLater()

        self.__thread_wait_list.clear()
        self.__count = 0
        self.thread_count_changed.emit(len(self.__thread_wait_list))
        self.__remove_flag = False

    def change_messages_enter_animation(self, value: QEasingCurve) -> None:
        self.__clean_all()
        self.__animation_by_combo_box = value

    def change_messages_anim_duration(self, value: float) -> None:
        self.__clean_all()
        self.__duration_by_combo_box = value

    def __check_message_anim_status(self) -> bool:
        return any([m.animate for m in self.__message_list])


    @pyqtSlot(MessageWidget)
    def add(self, message: MessageWidget) -> None:

        if not self.__check_message_anim_status() and self.__count <= self.__limit - 1:

            message.enter_animation = self.__animation_by_combo_box
            message.anim_duration = self.__duration_by_combo_box
            message.delete_signal.connect(self.__remove)
            message.animation_finished_signal.connect(self.__release_threads)
            message.show()
            message.activateWindow()
            message.raise_()

            self.__message_list.insert(0, message)

            self.__count += 1
            self.__reallocate()
            if message.from_threading:
                self.thread_count_changed.emit(len(self.__thread_wait_list))

        else:
            message.from_threading = True
            self.__thread_wait_list.insert(0, MessageThread(message=message, parent=self))
            self.thread_count_changed.emit(len(self.__thread_wait_list))

    def __reindex(self) -> None:
        #Reverse
        for count, message in enumerate(self.__message_list):
            message.index = len(self.__message_list) - count

    def __release_threads(self) -> None:
        size: int = len(self.__thread_wait_list)
        # Para não ficar em loop entre thread é necessário usar a flag self.__remove_flag enquando remove todas as mensagens
        if size > 0 and not self.__remove_flag:
            current: MessageThread = self.__thread_wait_list.pop(-1)
            current.add_signal.connect(self.add)
            current.finished.connect(current.deleteLater)
            current.start()

    @pyqtSlot(MessageWidget)
    def __remove(self, message: MessageWidget) -> None:

        if not message.animate:
            if message in self.__message_list:
                self.__message_list.remove(message)
                self.__count -= 1
                self.__reallocate(message)
                message.deleteLater()
                self.__release_threads()

    def __reallocate(self, current_message: MessageWidget = None) -> None:

        self.__reindex()
        if current_message is not None:
            index: int = current_message.update_index
            for count, message in enumerate(self.__message_list):
                if message.index < index:
                    message.animation_in(count, self.__offset, 'backward')


        else:
            for count, message in enumerate(self.__message_list):
                message.animation_in(count, self.__offset)
