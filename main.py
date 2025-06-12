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
        plugin_manager.walk("")

        if "-h" in sys.argv:
            print("Available plugins: ", ", ".join(f"--{p.lower()}" for p in plugin_manager.modules.keys()))
            exit(0)

        for tab_id, name in enumerate(plugin_manager.modules):
            if one and name != one:
                continue
            plugin: PluginBase = plugin_manager.modules[name]
            print()
            print(tab_id, plugin.ORDER, name, " python module:", plugin)

            if not plugin.isEnable():
                # plugin is not for this desktop or config
                continue

            # create zone
            widget_class = plugin.get_class()  # get widjet class
            if widget_class:
                print("  main class imported by plugin:", widget_class)
                if widget := widget_class(self):  # create instance of widget
                    print("  add vue:", widget)
                    if isinstance(self.tabs, QTabWidget):
                        self.tabs.addTab(widget, plugin.getIcon(), "")
                    else:
                        self.tabs.addWidget(widget)

            # create menu/btn entries
            if not one:
                action = QAction(plugin.getIcon(), plugin.getTitle(), self)
                action.triggered.connect(partial(self.change_module, tab_id, plugin.NAME))
                self.toolbar.addAction(action)

    def change_module(self, id_, title):
        tab = self.tabs
        tab.setCurrentIndex(id_)
        # print("page:", tab.currentIndex(), "/", tab.count())
        self.setWindowTitle("My App with plugins : " + title)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
