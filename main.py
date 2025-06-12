#!/usr/bin/env python
from functools import partial
from plugins._plugin.base import PluginBase, PluginManager

from PySide6.QtCore import Qt
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App with plugins")
        self.setMinimumHeight(200)

        # self.tabs = QTabWidget()
        # self.tabs.setTabPosition(QTabWidget.TabPosition.East)
        self.tabs = QStackedLayout()

        widget = QWidget()
        widget.setLayout(self.tabs)
        self.setCentralWidget(widget)
        # self.setCentralWidget(self.tabs)

        self.toolbar = QToolBar("My main toolbar")
        self.addToolBar(self.toolbar)
        self._init_plugins()

    def _init_plugins(self):
        plugin_manager = PluginManager()
        plugin_manager.walk("")

        for tab_id, name in enumerate(plugin_manager.modules):
            obj_plug: PluginBase = plugin_manager.modules[name]
            print()
            print(tab_id, obj_plug.ORDER, name, " python module:", obj_plug)
            print(" ", obj_plug.NAME)

            if not obj_plug.isEnable():
                # plugin is not for this desktop or config
                continue

            # create zone
            widget_class = obj_plug.get_class()  # get widjet class
            if widget_class:
                print("  main class imported by plugin:", widget_class)
                if widget := widget_class(self):  # create instance of widget
                    print("  add vue:", widget)
                    # self.tabs.addTab(widget, obj_plug.NAME)
                    self.tabs.addWidget(widget)

            # create menu/btn entries
            # we have some functions without create object (icon, title, ...)
            action = QAction(obj_plug.getIcon(), obj_plug.getTitle(), self)
            action.triggered.connect(partial(self.change_module, tab_id))
            self.toolbar.addAction(action)

    def change_module(self, id_):
        tab = self.tabs
        tab.setCurrentIndex(id_)
        print("page:", tab.currentIndex(), "/", tab.count())


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
