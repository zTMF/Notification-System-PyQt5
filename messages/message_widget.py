import os
import random
import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QPropertyAnimation, QEasingCurve, QPoint, QAbstractAnimation, QRect, \
    QVariant
from PyQt5.QtGui import QShowEvent, QResizeEvent
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGraphicsDropShadowEffect, QPushButton

from messages.utils import MessageType

sys.path.append(os.path.dirname(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/message.ui'), resource_suffix='')


class MessageWidget(QWidget, FORM_CLASS):
    delete_signal: pyqtSignal = pyqtSignal(QWidget)
    animation_finished_signal: pyqtSignal = pyqtSignal()

    def __init__(self, parent: QWidget = None) -> None:
        super(MessageWidget, self).__init__(parent)
        self.setupUi(self)
        self.__message_type: MessageType = MessageType.Success
        self.__height: int = 80
        self.__width: int = 350
        self.__top_offset: int = 0
        self.__message_index: int = 0
        self.__anim_on: bool = False
        self.__anim2_on: bool = False
        self.__flag_first_time: bool = False
        self.__from_threading: bool = False
        self.__enter_animation: QEasingCurve = QEasingCurve.OutBack
        self.__anim_duration: float = 0.5
        self.__progress_time: int = 5
        self.last_pos: QPoint = self.pos()

        self.__pos_anim = QPropertyAnimation(self, b'pos')
        self.__pos_anim.stateChanged.connect(self.__state_move_change)
        #self.__pos_anim.setDuration(int(self.__anim_duration * 1000))
        self.__pos_anim.setDuration(500)
        self.__pos_anim_close: QPropertyAnimation = QPropertyAnimation(self, b'pos')
        self.__progress_animation = QPropertyAnimation(self.progressBar, b"value")

        self.so_back = False


    @property
    def progress_time(self) -> int:
        return self.__progress_time

    @progress_time.setter
    def progress_time(self, value: int) -> None:
        self.__progress_time = value

    @property
    def anim_duration(self) -> float:
        return self.__anim_duration

    @anim_duration.setter
    def anim_duration(self, value: float) -> None:
        self.__anim_duration = value

    @property
    def enter_animation(self) -> QEasingCurve:
        return self.__enter_animation

    @enter_animation.setter
    def enter_animation(self, value: QEasingCurve) -> None:
        self.__enter_animation = value

    @property
    def from_threading(self) -> bool:
        return self.__from_threading

    @from_threading.setter
    def from_threading(self, value: bool) -> None:
        self.__from_threading = value

    @property
    def animate(self) -> bool:
        return self.__anim_on

    @animate.setter
    def animate(self, status: bool) -> None:
        self.__anim_on = status

    @property
    def close_animate(self) -> bool:
        return self.__anim2_on

    @close_animate.setter
    def close_animate(self, status: bool) -> None:
        self.__anim2_on = status

    @property
    def update_index(self) -> int:
        return self.__message_index

    @update_index.setter
    def update_index(self, index: int) -> None:
        self.__message_index = index
        self.label.setText(str(self.__message_index))


    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.__enter()
        self.update_message()

    @pyqtSlot()
    def __remove_message(self) -> None:
        self.delete_signal.emit(self)

    def __enter(self) -> None:

        self.__width: int = self.parent().width()

        effect = QGraphicsDropShadowEffect()
        effect.setOffset(0, 3)
        effect.setBlurRadius(10)
        self.setGraphicsEffect(effect)

        self.closeButton.clicked.connect(self.__close_animation)
        self.setFixedSize(self.__width, self.__height)
        self.__centralize()
        self.setGeometry(QRect(0, -self.__height, self.__width, self.__height))

    def move_animation(self, index: int, offset: int, direction: QAbstractAnimation = 'forward') -> None:

        self.last_pos = self.pos()
        self.__pos_anim.setEasingCurve(QEasingCurve(self.enter_animation))

        if direction == 'forward':
            self.__pos_anim.setStartValue(self.pos())
            if index == 0:
                self.__pos_anim.setEndValue(self.pos() + QPoint(0, self.height() + self.__top_offset))
            else:
                self.__pos_anim.setEndValue(self.pos() + QPoint(0, offset))
        else:
            self.so_back = True
            self.__pos_anim.setStartValue(self.pos())
            self.__pos_anim.setEndValue(self.last_pos - QPoint(0, offset))

        self.__pos_anim.start()




    def __progress_animation_run(self) -> None:

        self.__progress_animation.finished.connect(self.__close_animation)
        self.__progress_animation.valueChanged.connect(self.update)
        self.__progress_animation.setDuration(self.__progress_time * 1000)
        self.__progress_animation.setStartValue(self.progressBar.minimum())
        self.__progress_animation.setEndValue(self.progressBar.maximum())
        #self.__progress_animation.start()



    def __state_move_change(self, state: int) -> None:
        if state == QAbstractAnimation.Running:
            self.animate = True
        elif state == QAbstractAnimation.Stopped:
            self.animate = False
            if not self.__flag_first_time:
                self.__progress_animation_run()
                self.__flag_first_time = True
            self.animation_finished_signal.emit()

    def __state_close_change(self, state: int) -> None:
        if state == QAbstractAnimation.Running:
            self.close_animate = True
        elif state == QAbstractAnimation.Stopped:
            self.close_animate = False
            self.__progress_animation.deleteLater()
            self.__remove_message()

    def force_close_animation(self) -> None:
        self.__close_animation(False)

    @pyqtSlot()
    def __close_animation(self, with_signal: bool = True) -> None:
        '''if self.animate:
            print('Running animation')
            return'''

        #Prevent remove Message by button while animation run's
        if isinstance(self.sender(), QPushButton):
            if self.animate:
                print('Animate is running')
                return



        self.__pos_anim_close = QPropertyAnimation(self, b'pos')
        if with_signal:
            self.__pos_anim_close.stateChanged.connect(self.__state_close_change)
        else:
            self.__pos_anim_close.finished.connect(self.deleteLater)
        self.__pos_anim_close.setDuration(100)
        self.__pos_anim_close.setStartValue(self.pos())
        self.__pos_anim_close.setEndValue(self.pos() + QPoint(self.parent().width() - 20, 0))
        self.__pos_anim_close.start(QPropertyAnimation.DeleteWhenStopped)

    def __centralize(self) -> None:
        parent_center: QPoint = self.parent().rect().center()
        center: QPoint = self.rect().center()
        self.move(parent_center - center)

    @staticmethod
    def get_parent_color(color: str, value: int = 30) -> str:
        replace_list = ['rgb', '(', ')']
        for re in replace_list:
            color = color.replace(re, '')

        color_split = color.split(',')

        r = int(color_split[0])
        g = int(color_split[1])
        b = int(color_split[2])

        r -= value
        g -= value
        b -= value

        return f'rgb({r}, {g}, {b})'

    def update_message(self) -> None:
        raise NotImplemented
