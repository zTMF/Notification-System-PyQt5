import os
import random
import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QPropertyAnimation, QEasingCurve, QPoint, QAbstractAnimation, QRect, \
    QVariant, QSize
from PyQt5.QtGui import QShowEvent, QResizeEvent, QMovie
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGraphicsDropShadowEffect, QPushButton

from messages.utils import MessageType

sys.path.append(os.path.dirname(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/message.ui'), resource_suffix='')


class MessageWidget(QWidget, FORM_CLASS):
    delete_signal: pyqtSignal = pyqtSignal(bool)
    animation_finished_signal: pyqtSignal = pyqtSignal()
    anim_out_signal: pyqtSignal = pyqtSignal()

    def __init__(self, parent: QWidget = None) -> None:
        super(MessageWidget, self).__init__(parent)
        self.setupUi(self)
        self.__message_type: MessageType = MessageType.Success
        self.__height: int = 80
        self.__width: int = 350
        self.__top_offset: int = 0
        self.__anim_on: bool = False
        self.__anim2_on: bool = False
        self.__flag_first_time: bool = False
        self.__from_threading: bool = False
        self.__enter_animation: QEasingCurve = QEasingCurve.OutBack
        self.__anim_duration: float = 0.5
        self.__progress_time: int = 5
        self.__percent: float = 0.0
        self.last_pos: QPoint = self.pos()

        self.__movie = QMovie(os.path.join(os.path.dirname(__file__), '../images', 'spinner.gif'))
        self.__label_movie = QLabel(self.frame_2)
        self.__label_movie.setFixedSize(30, 30)
        self.__label_movie.setMovie(self.__movie)

        self.__pos_anim = QPropertyAnimation(self, b'pos')
        self.__pos_anim.stateChanged.connect(self.__state_move_change)
        

        self.__pos_anim_close: QPropertyAnimation = QPropertyAnimation(self, b'pos')
        self.progress_animation = QPropertyAnimation(self.progressBar, b"value")

    @property
    def progress(self) -> float:
        return self.__percent

    @progress.setter
    def progress(self, value: float) -> None:
        self.__percent = value

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

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.__enter()
        self.update_message()

    @pyqtSlot()
    def __remove_message(self) -> None:
        if isinstance(self.sender(), QPushButton):
            if self.progress_animation.state() == QAbstractAnimation.Running:
                try:
                    self.progress_animation.disconnect()
                except Exception as e:
                    print(e)
            self.delete_signal.emit(True)
        else:
            self.delete_signal.emit(False)

    def __enter(self) -> None:

        self.__width: int = self.parent().width()

        effect = QGraphicsDropShadowEffect()
        effect.setOffset(0, 3)
        effect.setBlurRadius(10)
        self.setGraphicsEffect(effect)

        self.closeButton.clicked.connect(self.__remove_message)
        self.setFixedSize(self.__width, self.__height)
        self.__centralize()
        self.setGeometry(QRect(0, -self.__height, self.__width, self.__height))

        rect: QRect = self.__label_movie.geometry()
        size: QSize = QSize(min(rect.width(), rect.height()), min(rect.width(), rect.height()))
        movie: QMovie = self.__label_movie.movie()
        movie.setScaledSize(size)
        self.__label_movie.move((self.frame_2.width() - self.__label_movie.width())/2, (self.frame_2.height() - self.__label_movie.height())/2)
        self.__label_movie.hide()

    def loading(self, state: bool = True) -> None:
        if state:
            self.__movie.start()
            self.__label_movie.show()
            self.closeButton.hide()
        else:
            self.__movie.stop()
            self.__label_movie.hide()
            self.closeButton.show()

    def animation_in(self, index: int = 0, offset: int = 50, direction: str = 'forward') -> None:
        self.last_pos = self.pos()
        self.__pos_anim.setDuration(int(self.__anim_duration * 1000))
        self.__pos_anim.setEasingCurve(QEasingCurve(self.enter_animation))
        if direction == 'forward':
            self.__pos_anim.setStartValue(self.pos())
            if index == 0:
                self.__pos_anim.setEndValue(self.pos() + QPoint(0, self.height() + self.__top_offset))
            else:
                self.__pos_anim.setEndValue(self.pos() + QPoint(0, offset))
        else:
            self.__pos_anim.setStartValue(self.pos())
            self.__pos_anim.setEndValue(self.last_pos - QPoint(0, offset))

        self.__pos_anim.start()

    def __progress_animation_run(self) -> None:

        self.progress_animation.finished.connect(self.__remove_message)
        self.progress_animation.valueChanged.connect(self.__on_progress_animation_value_changed)
        self.progress_animation.setDuration(self.__progress_time * 1000)
        self.progress_animation.setStartValue(self.progressBar.minimum())
        self.progress_animation.setEndValue(self.progressBar.maximum())

        self.progress_animation.start()

    @pyqtSlot(QVariant)
    def __on_progress_animation_value_changed(self, value: QVariant) -> None:
        percent: float = 100 * float(value) / float(self.progressBar.maximum())
        self.progress = percent
        self.update()

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
            self.anim_out_signal.emit()

    def force_close_animation(self) -> None:
        self.progress_animation.deleteLater()
        self.animate_out(False)

    @pyqtSlot()
    def animate_out(self, with_signal: bool = True) -> None:
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
