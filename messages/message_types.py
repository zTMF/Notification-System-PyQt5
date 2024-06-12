from PyQt5.QtWidgets import QWidget

from messages.new_message_widget import MessageWidget
from messages.utils import MessageType


class AlertMessage(MessageWidget):
    def __init__(self, message: str, parent: QWidget = None):
        super(AlertMessage, self).__init__(parent)
        self.__message = message

    def update_message(self) -> None:

        self.setStyleSheet(f'''
                #frame{{
                    background-color: {MessageType.Alert[0]};
                    border-radius: 5px;
                }}

                #label{{
                    color: white;
                }}
                ''')
        self.closeButton.setStyleSheet(f'''
                QPushButton{{
                    border: 2px solid {MessageType.Alert[0]};	
                    background-color: {MessageType.Alert[0]};
                    color:  {MessageType.Alert[1]};
                    border-radius: 5px;
                }}



                QPushButton::hover{{
                    background-color: {self.get_parent_color(MessageType.Alert[0])};
                }}

                ''')
        self.label.setText(self.__message)
        self.label.setStyleSheet(f'''
                QLabel{{
                    color: {MessageType.Alert[1]};
                }}
        ''')

        self.progressBar.setStyleSheet(f'''
                QProgressBar{{
                    border-radius: 5px;
                    background-color: {MessageType.Alert[0]};
                }}
                QProgressBar::chunk{{
                    background-color:{self.get_parent_color(MessageType.Alert[0], 50)};
                }}
        '''
        )



class ErrorMessage(MessageWidget):

    def __init__(self, message: str, parent: QWidget = None) -> None:
        super(ErrorMessage, self).__init__(parent)
        self.__message: str = message


    def update_message(self) -> None:

        self.setStyleSheet(f'''
                        #frame{{
                            background-color: {MessageType.Error[0]};
                            border-radius: 5px;
                        }}

                        #label{{
                            color: white;
                        }}
                        ''')
        self.closeButton.setStyleSheet(f'''
                        QPushButton{{
                            border: 2px solid {MessageType.Error[0]};	
                            background-color: {MessageType.Error[0]};
                            color:  {MessageType.Error[1]};
                            border-radius: 5px;
                        }}



                        QPushButton::hover{{
                            background-color: {self.get_parent_color(MessageType.Error[0])};
                        }}

                        ''')
        self.label.setText(self.__message)
        self.label.setStyleSheet(f'''
                        QLabel{{
                            color: {MessageType.Error[1]};
                        }}
                ''')
        self.progressBar.setStyleSheet(f'''
                        QProgressBar{{
                            border-radius: 5px;
                            background-color: {MessageType.Error[0]};
                        }}
                        QProgressBar::chunk{{
                            background-color:{self.get_parent_color(MessageType.Error[0], 50)};
                        }}
                ''')

class SuccessMessage(MessageWidget):
    def __init__(self, message: str, parent: QWidget = None):
        super(SuccessMessage, self).__init__(parent)
        self.__message: str = message

    def update_message(self) -> None:

        self.setStyleSheet(f'''
                        #frame{{
                            background-color: {MessageType.Success[0]};
                            border-radius: 5px;
                        }}

                        #label{{
                            color: white;
                        }}
                        ''')
        self.closeButton.setStyleSheet(f'''
                        QPushButton{{
                            border: 2px solid {MessageType.Success[0]};	
                            background-color: {MessageType.Success[0]};
                            color:  {MessageType.Success[1]};
                            border-radius: 5px;
                        }}



                        QPushButton::hover{{
                            background-color: {self.get_parent_color(MessageType.Success[0])};
                        }}

                        ''')
        self.label.setText(self.__message)
        self.label.setStyleSheet(f'''
                        QLabel{{
                            color: {MessageType.Success[1]};
                        }}
                ''')
        self.progressBar.setStyleSheet(f'''
                                QProgressBar{{
                                    border-radius: 5px;
                                    background-color: {MessageType.Success[0]};
                                }}
                                QProgressBar::chunk{{
                                    background-color:{self.get_parent_color(MessageType.Success[0], 50)};
                                }}
                        ''')

class WarningMessage(MessageWidget):
    def __init__(self, message: str, parent: QWidget =None):
        super(WarningMessage, self).__init__(parent)
        self.__message = message

    def update_message(self) -> None:

        self.setStyleSheet(f'''
                #frame{{
                    background-color: {MessageType.Warning[0]};
                    border-radius: 5px;
                }}

                #label{{
                    color: white;
                }}
                ''')
        self.closeButton.setStyleSheet(f'''
                QPushButton{{
                    border: 2px solid {MessageType.Warning[0]};	
                    background-color: {MessageType.Warning[0]};
                    color:  {MessageType.Warning[1]};
                    border-radius: 5px;
                }}



                QPushButton::hover{{
                    background-color: {self.get_parent_color(MessageType.Warning[0])};
                }}

                ''')
        self.label.setText(self.__message)
        self.label.setStyleSheet(f'''
                QLabel{{
                    color: {MessageType.Warning[1]};
                }}
        ''')
        self.progressBar.setStyleSheet(f'''
                                QProgressBar{{
                                    border-radius: 5px;
                                    background-color: {MessageType.Warning[0]};
                                }}
                                QProgressBar::chunk{{
                                    background-color:{self.get_parent_color(MessageType.Warning[0], 50)};
                                }}
                        ''')