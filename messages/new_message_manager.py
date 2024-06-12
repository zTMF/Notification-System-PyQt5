import itertools
import math
from queue import Queue
from threading import Lock

from PyQt5.QtCore import QObject, pyqtSlot, QEasingCurve, pyqtSignal, QTimerEvent, QTimer
from PyQt5.QtWidgets import QWidget

from messages.new_message_widget import MessageWidget


class MessageManager(QObject):
    thread_count_changed: pyqtSignal = pyqtSignal(int)

    def __init__(self, max_messages: int = 3, offset: int = 50, parent: QWidget = None):
        super(MessageManager, self).__init__(parent)
        self.__max_messages: int = max_messages
        self.__offset: int = offset
        self.__visible_messages: list = []
        self.__message_queue: Queue = Queue()
        self.__message_wait_delete: list = []
        self.__lock: Lock = Lock()
        self.__animation_by_combo_box: QEasingCurve = QEasingCurve.OutBack
        self.__remove_flag: bool = False
        self.__duration_by_combo_box: float = 0.5

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__release_remove)
        self.__timer.setInterval(100)

    def __qtimer_process(self, state: bool):
        if not state:
            if self.__timer.isActive():
                self.__timer.stop()
                # print("Pausou a fila para remover")
            else:
                pass
                # print("Já está pausado")
        else:
            if not self.__timer.isActive():
                self.__timer.start()
                # print("Retomou a fila para remover")
            else:
                pass

    def __clean_all(self) -> None:
        self.__remove_flag = True
        # Messages Running
        for message in self.__visible_messages:
            message.force_close_animation()
        self.__visible_messages.clear()

        # In Queue Messages
        for _ in range(self.__message_queue.qsize()):
            message: MessageWidget = self.__message_queue.get()
            message.deleteLater()

        self.__message_queue.queue.clear()
        self.thread_count_changed.emit(self.__message_queue.qsize())

        self.__remove_flag = False

    def change_messages_enter_animation(self, value: QEasingCurve) -> None:
        self.__clean_all()
        self.__animation_by_combo_box = value

    def change_messages_anim_duration(self, value: float) -> None:
        self.__clean_all()
        self.__duration_by_combo_box = value

    def __check_message_anim_status(self) -> bool:
        return any([m.animate for m in self.__visible_messages])

    def __check_message_anim_out_status(self) -> bool:
        return any([m.close_animate for m in self.__visible_messages])

    def add(self, message: MessageWidget) -> None:
        if self.__remove_flag:
            return
        with self.__lock:
            if len(self.__visible_messages) < self.__max_messages and not self.__check_message_anim_status() and not self.__check_message_anim_out_status():
                self.__qtimer_process(False)
                self.__visible_messages.insert(0, message)
                self.__show(message)
            else:
                self.__message_queue.put(message)

        self.thread_count_changed.emit(self.__message_queue.qsize())

    def __show(self, message: MessageWidget) -> None:

        message.enter_animation = self.__animation_by_combo_box
        message.anim_duration = self.__duration_by_combo_box
        message.delete_signal.connect(self.__queue_message)
        message.animation_finished_signal.connect(self.__check_queue)
        message.anim_out_signal.connect(self.__remove)
        message.show()
        message.activateWindow()
        message.raise_()
        self.__reallocate()

    @pyqtSlot(bool)
    def __queue_message(self, priority: bool) -> None:
        message: MessageWidget = self.sender()
        with self.__lock:
            if message not in self.__message_wait_delete:
                message.loading(True)
                if priority:
                    self.__message_wait_delete.insert(0, message)
                else:
                    self.__message_wait_delete.append(message)

        print(len(self.__message_wait_delete))

    @pyqtSlot()
    def __remove(self):

        message: MessageWidget = self.sender()
        message.loading(False)
        self.__reallocate(message)
        self.__visible_messages.remove(message)
        message.deleteLater()
        self.__check_queue()

    @pyqtSlot()
    def __release_remove(self) -> None:
        if len(self.__message_wait_delete) > 0:
            if not self.__check_message_anim_out_status() and not self.__check_message_anim_status():
                current: MessageWidget = self.__message_wait_delete.pop(0)
                current.animate_out()

        else:
            if len(self.__visible_messages) == 0:
                self.__qtimer_process(False)

    def __check_queue(self) -> None:
        self.__qtimer_process(True)
        if not self.__message_queue.empty():
            next_message: MessageWidget = self.__message_queue.get()
            self.add(next_message)

    def __reallocate(self, current_message: MessageWidget = None) -> None:

        if current_message is not None:
            start_index: int = self.__visible_messages.index(current_message)
            for count, message in enumerate(self.__visible_messages[start_index:]):
                message.animation_in(count, self.__offset, 'backward')
        else:
            for count, message in enumerate(self.__visible_messages):
                message.animation_in(count, self.__offset)
