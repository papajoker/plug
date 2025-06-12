from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel


class KernelMain(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setWindowTitle("Manage manjaro kernels")

        self.setStyleSheet("background-color: #380;")
        QLabel("linux122", parent=self, margin=20)


class Plugin:
    NAME = "Kernels"
    ORDER = 10  # 10 by 10, order in main app

    @classmethod
    def getTitle(cls) -> str:
        return cls.NAME

    @staticmethod
    def getIcon() -> QIcon:
        return QIcon.fromTheme(QIcon.ThemeIcon.Computer)

    @staticmethod
    def isEnable() -> bool:
        return True

    @staticmethod
    def get_class():
        # return class and not instance
        return KernelMain