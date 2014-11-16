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
        super(MainWindow, self).__init__(None)
        self.default_bead = BeadType('blank', QBrush(QColor(230, 230, 228)))

        self.create_central_widget()
        self.create_menu_bar()
        self.create_tool_bar()
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


    def open_design(self):
        """Slot that opens a design in a new tab."""
        extension = '.peyd'
        (paths, flt) = QFileDialog.getOpenFileNames(parent=self, caption='Open Design',
                                                  filter='Peyote Design (*{})'.format(extension))

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
            (path, flt) = QFileDialog.getSaveFileName(self, 'Save Design',
                                               './{}{}'.format(design.name, design_extension),
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
        (path, flt) = QFileDialog.getSaveFileName(self, 'Save Design',
                                                  './{}{}'.format(design.name, design_extension),
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
    # pattern_area = PatternArea()
    # pattern_area.show()

    sys.exit(app.exec_())
