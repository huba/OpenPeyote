#!/usr/bin/env python3
"""
OpenPeyote. A program for designing patterns to be made with the
Peyote beading technique.
Author: Huba Z. Nagy (12huba@gmail.com)
Date: 10.11.2014
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from design_widget import *
from catalog_widget import *
from wizards_and_dialogs import *



class MainWindow(QMainWindow):

    """The main application window."""
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.default_bead = BeadType('blank', QBrush(QColor(230, 230, 228)))

        self.create_central_widget()
        self.create_menu_bar()
        self.create_docked_widgets()


    def create_central_widget(self):
        """Sets up the multiple document interface."""
        self.mdi_widget = QMdiArea()
        self.mdi_widget.setViewMode(QMdiArea.TabbedView)

        self.setCentralWidget(self.mdi_widget)


    def create_menu_bar(self):
        # the file menu...
        file_menu = self.menuBar().addMenu('File')

        new_action = file_menu.addAction('New Design')
        new_action.setShortcuts(QKeySequence.New)
        new_action.triggered.connect(self.new_design)

        open_action = file_menu.addAction('Open Design')
        open_action.setShortcuts(QKeySequence.Open)

        # the edit menu...
        # TODO: all the menus and etc


    def create_status_bar(self):
        pass


    def create_docked_widgets(self):
        self.catalog = Catalog()
        self.working_bead = self.default_bead
        self.addDockWidget(Qt.LeftDockWidgetArea, self.catalog)
        self.catalog.catalog_tree.currentItemChanged.connect(self.select_type)

        # Adding a test collection to the catalog
        new_collection = Collection('Test set')

        new_bead_type = BeadType('Test red', Qt.red)
        new_collection.addChild(new_bead_type)

        new_bead_type = BeadType('Test blue', Qt.blue)
        new_collection.addChild(new_bead_type)

        self.catalog.add_collection(new_collection)


    def new_design(self):
        """Slot for creating a new design. This function summons Gandalf who will help
        the user with creating their design."""
        # TODO: hmmm this generates a weird message, might need to look at that...
        # Also there are some performance problems...
        wizard = NewWizard(self)
        wizard.exec_()


    def select_type(self, new_selection, prev_selection):
        """Slot used to select a type of bead."""
        if new_selection.type() == 1001:
            self.working_bead = new_selection



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.create()
    mw.showMaximized()
    # pattern_area = PatternArea()
    # pattern_area.show()

    sys.exit(app.exec_())
