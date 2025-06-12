#!/usr/bin/env python
from functools import partial
from plugins._plugin.base import PluginBase, PluginManager
import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedLayout,
    QTabWidget,
    QToolBar,
    QWidget,
)


class MainWindow(QMainWindow):
    USE_TABS = True

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App with plugins")
        self.resize(600, 450)

        if self.USE_TABS:
            self.tabs = QTabWidget()  # TODO rewrite paint() for display icon + text in tab
            self.tabs.setTabPosition(QTabWidget.TabPosition.East)
            self.tabs.setIconSize(QSize(42, 42))
            self.tabs.setTabBarAutoHide(True)
            self.tabs.setStyleSheet("QTabBar::tab { min-width: 100px;  alignment: center;}")
        else:
            self.tabs = QStackedLayout()
        self.tabs.currentChanged.connect(self.module_changed)

        if isinstance(self.tabs, QTabWidget):
            self.setCentralWidget(self.tabs)
        else:
            widget = QWidget()
            widget.setLayout(self.tabs)
            self.setCentralWidget(widget)

        self.toolbar = QToolBar("modules")
        self.toolbar.setMovable(False)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        self._init_plugins()

    def _init_plugins(self):
        one = ""
        if args := [a.removeprefix("--").lower() for a in sys.argv if a.startswith("--")]:
            one = args[0]
            self.toolbar.setVisible(False)
            print("load one plugin ?", one)

        plugin_manager = PluginManager()
        plugin_manager.scan("")

        if "-h" in sys.argv:
            print("Available plugins: ", ", ".join(f"--{p.lower()}" for p in plugin_manager.modules.keys()))
            exit(0)

        for name in plugin_manager.modules:
            if one and name != one:
                continue
            plugin: PluginBase = plugin_manager.modules[name]
            print()
            print(plugin.ORDER, name, " python module:", plugin)

            if not plugin.isEnable():
                # plugin is not for this desktop or config
                continue

            # create zone
            widget_class = plugin.get_class()  # get widjet class
            if not widget_class or not issubclass(widget_class, QWidget):
                continue

            print("  main class imported by plugin:", widget_class)

            widget = widget_class(self)
            if not widget:
                continue

            print("  add view:", widget)

            if isinstance(self.tabs, QTabWidget):
                tab_id = self.tabs.addTab(widget, plugin.getIcon(), "")
            else:
                tab_id = self.tabs.addWidget(widget)

            # create menu/btn entries
            action = QAction(plugin.getIcon(), plugin.getTitle(), self)
            action.triggered.connect(partial(self.change_module, tab_id, plugin.NAME))
            self.toolbar.addAction(action)

    def module_changed(self, tab_id: int):
        self.setWindowTitle(self.tabs.currentWidget().windowTitle())

    def change_module(self, tab_id: int, title: str):
        self.tabs.setCurrentIndex(tab_id)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
