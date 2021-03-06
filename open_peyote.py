#!/usr/bin/env python3
"""
OpenPeyote. A program for designing patterns to be made with the
Peyote beading technique.
Author: Huba Z. Nagy (12huba@gmail.com)
Date: 10.11.2014
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import json

from design_widget import *
from catalog_widget import *
from wizards_and_dialogs import *
from util import *



class MainWindow(QMainWindow):
    """The main application window."""
    def __init__(self):
        """Init function for the main application."""
        super(MainWindow, self).__init__(None)
        self.default_bead = BeadType('blank', 'n/a', QBrush(QColor(230, 230, 228)), '#000000', '#000000', 10)

        # Calls the functions to prepare each area of the main window
        self.create_central_widget()
        self.create_menu_bar()
        self.create_tool_bar()
        self.create_docked_widgets()
        self.create_status_bar()


    def create_central_widget(self):
        """Sets up the multiple document interface."""
        self.mdi_widget = QMdiArea()
        self.mdi_widget.setViewMode(QMdiArea.TabbedView)

        self.setCentralWidget(self.mdi_widget)


    def create_menu_bar(self):
        """Adds all the menus and actions to the menu bar."""
        # the file menu...
        file_menu = self.menuBar().addMenu('File')

        new_action = file_menu.addAction('New Design')
        new_action.setShortcuts(QKeySequence.New)
        new_action.triggered.connect(self.new_design)

        open_action = file_menu.addAction('Open Design')
        open_action.setShortcuts(QKeySequence.Open)
        open_action.triggered.connect(self.open_design)

        save_action = file_menu.addAction('Save Design')
        save_action.setShortcuts(QKeySequence.Save)
        save_action.triggered.connect(self.save_design)

        save_as_action = file_menu.addAction('Save Design As')
        # TODO: look into why QKeySequence.SaveAs is not recognized in pyqt5
        # save_as_action.setShortcuts(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_as)

        # the edit menu...
        # TODO: all the menus and etc


    def create_tool_bar(self):
        """Adds the tools to the toolbar."""
        edit_tool_bar = self.addToolBar('Edit')

        tool_group = QActionGroup(self)
        tool_group.setExclusive(True)

        self.bead_tool_action = edit_tool_bar.addAction('Bead Tool')
        self.bead_tool_action.setCheckable(True)
        tool_group.addAction(self.bead_tool_action)

        self.remove_tool_action = edit_tool_bar.addAction('Clear Tool')
        self.remove_tool_action.setCheckable(True)
        tool_group.addAction(self.remove_tool_action)


    def create_status_bar(self):
        """Prepares the status bar"""
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage('Test', 2000)


    def create_docked_widgets(self):
        """Adds the docked widget."""
        self.catalog = Catalog()
        self.working_bead = self.default_bead

        catalog_dock = QDockWidget()
        catalog_dock.setWidget(self.catalog)
        catalog_dock.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        catalog_dock.setWindowTitle('Catalog')
        self.addDockWidget(Qt.LeftDockWidgetArea, catalog_dock)
        self.catalog.currentItemChanged.connect(self.select_type)


    def new_design(self):
        """Slot for creating a new design. This function summons Gandalf who will help
        the user with creating their design."""
        # TODO: hmmm this generates a weird message, might need to look at that...
        # Also there are some performance problems...
        wizard = NewWizard(self)
        wizard.exec_()


    def open_design(self):
        """Slot that opens (a) design(s) in a new tab."""
        (paths, flt) = QFileDialog.getOpenFileNames(parent=self, caption='Open Design',
                                                  filter='Peyote Design (*{})'.format(design_extension))

        if flt == '':
            # it means they clicked cancel...
            return

        for path in paths:
            self._open_design(path)


    def _open_design(self, path):
        with open(path, 'r') as file:
            rdict = json.load(file)
            info = rdict['__info__']
            grid = rdict['__beads__']

            design = DesignScene(self,
                                 bgrid=grid,
                                 name=info['__name__'],
                                 track_width=info['__track_width__'],
                                 tracks=info['__tracks__'],
                                 height=info['__height__'])

            area = PatternArea(design=design)
            area.filepath = path
            self.mdi_widget.addSubWindow(area)


    def save_design(self):
        """Slot for saving the design in the active tab."""
        # TODO: handle no tabs being open, it would be a good idea if
        # the button was disabled when there are no tabs for example.
        design = self.mdi_widget.activeSubWindow().widget().scene()

        if not self.mdi_widget.activeSubWindow().widget().filepath:
            name_s = '_'.join(design.name.lower().split(' '))
            (path, flt) = QFileDialog.getSaveFileName(self, 'Save Design',
                                               './{}{}'.format(name_s, design_extension),
                                               'Peyote Design (*{})'.format(design_extension))

            if flt == '':
                # it means they clicked cancel...
                return

            self.mdi_widget.activeSubWindow().widget().filepath = path

        else:
            path = self.mdi_widget.activeSubWindow().widget().filepath

        with open(path, 'w') as file:
            json.dump(design.to_dict(), file)


    def save_as(self):
        """Save and force the user to select a new path"""
        design = self.mdi_widget.activeSubWindow().widget().scene()
        name_s = name_s = '_'.join(design.name.lower().split(' '))
        (path, flt) = QFileDialog.getSaveFileName(self, 'Save Design',
                                                  './{}{}'.format(name_s, design_extension),
                                                  'Peyote Design (*{})'.format(design_extension))

        if flt == '':
            # it means they clicked cancel...
            return

        self.mdi_widget.activeSubWindow().widget().filepath = path

        with open(path, 'w') as file:
            json.dump(design.to_dict(), file)


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

    sys.exit(app.exec_())
