# from ..plugin.base import PluginBase


from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel


class UserMain(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setWindowTitle("Manage users")

        self.setStyleSheet("background-color: #909;")
        QLabel("Super User", parent=self, margin=20)


class Plugin:
    NAME = "User"
    ORDER = 20  # 10 by 10, order in main app

    @classmethod
    def getTitle(cls) -> str:
        return cls.NAME

    @staticmethod
    def getIcon() -> QIcon:
        return QIcon.fromTheme(QIcon.ThemeIcon.GoHome)

    @staticmethod
    def isEnable() -> bool:
        # if kde : return False
        # or if wayland : return False ?
        return True

    @staticmethod
    def get_class():
        # return class and not instance
        return UserMain