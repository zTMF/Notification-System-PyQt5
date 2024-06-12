import random
import sys

from PyQt5.QtGui import QResizeEvent, QShowEvent, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import pyqtSlot, Qt


from messages.message_types import *
from messages.new_message_manager import MessageManager
from messages.utils import EasingCurve


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplicação de Mensagens")
        self.setGeometry(100, 100, 600, 400)

        self.__button: QPushButton = QPushButton("Clique", self)
        self.__button.setObjectName('mainButton')
        self.__button.clicked.connect(self.__button_clicked)

        self.__label: QLabel = QLabel("( 0 )", self.__button)
        self.__label.setFixedWidth(25)
        self.__label.setObjectName('mainLabel')

        self.__combo_box_animation: QComboBox = QComboBox(self)
        self.__combo_box_animation.currentIndexChanged.connect(self.__combo_box_animation_index_changed)
        self.__combo_box_animation_selected_indices: list = []

        self.__combo_box_duration: QComboBox = QComboBox(self)
        self.__combo_box_duration.currentIndexChanged.connect(self.__combo_box_duration_index_changed)

        self.__message_manager: MessageManager = MessageManager(max_messages=6, parent=self)
        self.__message_manager.thread_count_changed.connect(lambda value: self.__label.setText(str(value)))


    @pyqtSlot(int)
    def __combo_box_animation_index_changed(self, index: int) -> None:
        value = self.__combo_box_animation.itemData(index)

        self.__message_manager.change_messages_enter_animation(value)
        if index not in self.__combo_box_animation_selected_indices:
            self.__combo_box_animation_selected_indices.append(index)

        for index in range(self.__combo_box_animation.count()):
            if index in self.__combo_box_animation_selected_indices:
                self.__combo_box_animation.setItemData(index, QColor(Qt.yellow), Qt.BackgroundRole)
            else:
                self.__combo_box_animation.setItemData(index, QColor(Qt.white), Qt.BackgroundRole)


    @pyqtSlot(int)
    def __combo_box_duration_index_changed(self, index: int) -> None:

        value = self.__combo_box_duration.itemData(index)
        self.__message_manager.change_messages_anim_duration(value)

    def showEvent(self, event: QShowEvent) -> None:
        self.__update_main_widgets_position()
        for name in dir(EasingCurve):
            if not name.startswith('__'):
                self.__combo_box_animation.addItem(name, getattr(EasingCurve, name))

        count: int = 1*10
        for i in range(1, count + 1):
            self.__combo_box_duration.addItem(f'{i/10} sec', i/10)

    @pyqtSlot()
    def __button_clicked(self) -> None:

        '''
        4
        2
        7
        '''

        list_time = [7, 2, 7, 2]

        #for _ in range(len(list_time)):
        message_random_list: list = [SuccessMessage('Success', self),
                                     WarningMessage('Warning', self),
                                     AlertMessage('Alert', self),
                                     ErrorMessage('Error', self)]
        random_number: int = random.randint(0, len(message_random_list) - 1)
        current: MessageWidget = message_random_list[random_number]
        current.progress_time = random.randint(5, 10)
        self.__message_manager.add(current)


    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.__update_main_widgets_position()

    def __update_main_widgets_position(self) -> None:

        button_width: int = self.__button.width()
        button_height: int = self.__button.height()

        label_width: int = self.__label.width()
        label_height: int = self.__label.height()

        combo_box_animation_width: int = self.__combo_box_animation.width()
        combo_box_animation_height: int = self.__combo_box_animation.height()

        combo_box_duration_width: int = self.__combo_box_duration.width()
        combo_box_duration_height: int = self.__combo_box_duration.height()

        x: int = int((self.width() - button_width) / 2)
        y: int = int(self.height() - button_height - 20)
        self.__button.setGeometry(x, y, button_width, button_height)
        self.__combo_box_animation.setGeometry(x - combo_box_animation_width - 10, y, combo_box_animation_width,
                                               combo_box_animation_height)
        self.__combo_box_duration.setGeometry(x + button_width + 10, y, combo_box_duration_width, combo_box_duration_height)

        x_label: int = int(button_width - label_width - 15)
        y_label: int = int((button_height / 2) - (label_height / 2))
        self.__label.setGeometry(x_label, y_label, label_width, label_height)


def load_stylesheet(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stylesheet = load_stylesheet("styles/MainWindowStyle.qss")
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
