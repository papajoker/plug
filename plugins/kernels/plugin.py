from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel


class KernelMain(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background-color:#66bb00; ")
        QLabel("linux122", self)


class Plugin:
    NAME = "Kernels Manager"

    @classmethod
    def getTitle(cls) -> str:
        return cls.NAME

    @staticmethod
    def getIcon() -> QIcon:
        return QIcon.fromTheme(QIcon.ThemeIcon.ListAdd)

    @staticmethod
    def isEnable() -> bool:
        return True

    @staticmethod
    def order() -> int:
        return 10

    def app(self):
        # return class and not object
        return KernelMain