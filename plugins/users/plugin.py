# from ..plugin.base import PluginBase


from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel


class UserMain(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background-color: #cc00cc; ")
        QLabel("Super User", self)


class Plugin:
    NAME = "User Manager"
    ORDER = 20  # 10 by 10, order in main app

    @classmethod
    def getTitle(cls) -> str:
        return cls.NAME

    @staticmethod
    def getIcon() -> QIcon:
        return QIcon.fromTheme(QIcon.ThemeIcon.Computer)

    @staticmethod
    def isEnable() -> bool:
        # if kde : return False
        # or if wayland : return False ?
        return True

    def get_class(self):
        # return class and not object
        return UserMain