"""
As the name suggests this module defines all the wizards and dialogs.
Author: Huba Z. Nagy (12huba@gmail.com)
Date: 12.11.2014
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from design_model import *
from design_widget import *



class NewWizard(QWizard):
    def __init__(self, mw, parent=None):
        super(NewWizard, self).__init__(parent)
        self.addPage(DesignSpecsPage())

        self.setWindowTitle('Creating a New Design')
        self.mw = mw # just a handle so the new design can be
        # added to the main window...


    def accept(self):
        # Extracting information from the field
        name = self.field('design_name')
        track_width = self.field('track_width')
        width = self.field('width')
        height = self.field('height')

        # Creating the new design and adding it to the main window
        new_design = DesignScene(self.mw, name=name, track_width=track_width, tracks=width, height=height)
        new_area = PatternArea(design=new_design)
        self.mw.mdi_widget.addSubWindow(new_area)
        new_area.update()

        super(NewWizard, self).accept()



class DesignSpecsPage(QWizardPage):
    def __init__(self, parent=None):
        super(DesignSpecsPage, self).__init__(parent)
        self.setTitle('New Design Specifications')

        form = QFormLayout()

        design_name = QLineEdit()
        form.addRow('Design name:', design_name)
        self.registerField('design_name*', design_name)

        track_width = QSpinBox()
        track_width.setMaximum(4)
        track_width.setMinimum(1)
        form.addRow('Drop Width:', track_width)
        self.registerField('track_width', track_width)

        width = QSpinBox()
        width.setMinimum(1)
        form.addRow('Number of Drops:', width)
        self.registerField('width', width)

        height = QSpinBox()
        height.setMinimum(5)
        form.addRow('Height:', height)
        self.registerField('height', height)

        self.setLayout(form)
