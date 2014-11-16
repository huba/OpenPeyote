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

import catalog_widget



class NewWizard(QWizard):
    """This one creates new designs."""
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

    def initializePage(self):
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



class CollectionWizard(QWizard):
    def __init__(self, catalog, parent=None):
        super(CollectionWizard, self).__init__(parent)
        self.catalog = catalog

        self.setWindowTitle('Creating a New Bead Collection')
        self.addPage(CollectionSpecsPage())


    def accept(self):
        name = self.field('collection_name')

        new_collection = catalog_widget.Collection(name)
        self.catalog.add_collection(new_collection)
        super(CollectionWizard, self).accept()



class CollectionSpecsPage(QWizardPage):
    def __init__(self, parent=None):
        super(CollectionSpecsPage, self).__init__(parent)
        self.setTitle('Specifications of New Bead Collection')

    def initializePage(self):
        form = QFormLayout()

        collection_name = QLineEdit()
        form.addRow('Collection Name: ', collection_name)
        self.registerField('collection_name*', collection_name)

        self.setLayout(form)



class BeadWizard(QWizard):
    """This one creates new types of beads and adds them to a collection.
    I also keep misreading it as 'beard wizard'..."""
    def __init__(self, collection, parent=None):
        super(BeadWizard, self).__init__(parent)
        self.setWindowTitle('Creating a New Bead Type')
        self.addPage(BeadSpecsPage())
        self.addPage(BeadAppearancePage())

        self.collection = collection


    def accept(self):
        name = self.field('bead_name')
        catalog_number = self.field('catalog_number')
        brush = self.field('bead_brush')
        base_color = self.field('base_color')
        highlight_color = self.field('highlight_color')
        texture = self.field('texture')

        new_bead_type = catalog_widget.BeadType(name,
                                                catalog_number,
                                                brush,
                                                base_color,
                                                highlight_color,
                                                texture)
        self.collection.addChild(new_bead_type)
        super(BeadWizard, self).accept()



class BeadSpecsPage(QWizardPage):
    def __init__(self, parent=None):
        super(BeadSpecsPage, self).__init__(parent)
        self.setTitle('Specifications of New Bead')

    def initializePage(self):
        form = QFormLayout()

        bead_name = QLineEdit()
        form.addRow('Bead Name: ', bead_name)
        self.registerField('bead_name*', bead_name)

        catalog_number = QLineEdit()
        form.addRow('Catalog Number: ', catalog_number)
        self.registerField('catalog_number*', catalog_number)

        self.setLayout(form)



class BeadAppearancePage(QWizardPage):
    def __init__(self, parent=None):
        super(BeadAppearancePage, self).__init__(parent)
        self.setTitle('Appearance and Color')

    def initializePage(self):
        vbox = QVBoxLayout()

        # Top row of radio buttons
        hbox_t = QHBoxLayout()

        top_w = QWidget()
        matte_box = QRadioButton(top_w)
        matte_box.setText('Matte')
        hbox_t.addWidget(matte_box)

        shiny_box = QRadioButton(top_w)
        shiny_box.setText('Polished')
        hbox_t.addWidget(shiny_box)

        top_w.setLayout(hbox_t)
        vbox.addWidget(top_w)

        # Bottom row with form and the bead preview
        hbox_b = QHBoxLayout()

        form = QFormLayout()
        base_color = ColorButton(QColor('#aa0000'))
        form.addRow('Base Color: ', base_color)
        self.registerField('base_color', base_color, property='color_string')

        highlight_color = ColorButton(QColor('#ff0000'))
        form.addRow('Highlight Color: ', highlight_color)
        self.registerField('highlight_color', highlight_color, property='color_string')

        form_w = QWidget()
        form_w.setLayout(form)
        hbox_b.addWidget(form_w)

        demo_bead = DemoBead(base_color, highlight_color, shiny_box)
        shiny_box.toggled.connect(demo_bead.texture_change)
        self.registerField('bead_brush', demo_bead, property='brush')
        self.registerField('texture', demo_bead, property='texture')
        hbox_b.addWidget(demo_bead)

        bottom_w = QWidget()
        bottom_w.setLayout(hbox_b)
        vbox.addWidget(bottom_w)
        self.setLayout(vbox)



class ColorButton(QPushButton):
    """Button which calls a color dialog when clicked and it shows the color that is currently selected."""
    def __init__(self, selected_color, parent=None):
        super(ColorButton, self).__init__(parent)
        self.selected_color, self.demo_bead = selected_color, None
        self._color_string = self.selected_color.name()
        self.setStyleSheet('background-color:{}'.format(self._color_string))


    @pyqtProperty(str)
    def color_string(self):
        return self._color_string

    @color_string.setter
    def color_string(self, new_color):
        self._color_string = new_color

    def mousePressEvent(self, evt):
        """Summons the color dialog when clicked."""
        color_dialog = QColorDialog(self.selected_color)
        if color_dialog.exec_() == 1:
            # Only change the selected color if they click OK
            self.selected_color = color_dialog.currentColor()
            self._color_string = self.selected_color.name()
            self.setStyleSheet('background-color:{}'.format(self._color_string))

            if self.demo_bead:
                self.demo_bead.set_pixmap()



class DemoBead(QGraphicsView):
    """Shows a preview of the color settings."""
    brush_changed = pyqtSignal()
    def __init__(self, base_button, highlight_button, shiny, parent=None):
        super(DemoBead, self).__init__(parent)
        self._brush = QBrush(Qt.red)
        self._texture = MATTE
        self.setScene(QGraphicsScene())
        self.setBackgroundBrush(QBrush(QColor(190, 189, 184)))

        self.base_button, self.highlight_button, self.shiny = base_button, highlight_button, shiny
        self.base_button.demo_bead = self
        self.highlight_button.demo_bead = self

        self.pixmap_item = QGraphicsPixmapItem(QPixmap(28, 40))
        self.scene().addItem(self.pixmap_item)

        self.set_pixmap()


    # These expose the brush property to Qt's Wizard api.
    @pyqtProperty(QBrush)
    def brush(self):
        return self._brush

    @brush.setter
    def brush(self, new_brush):
        self._brush = new_brush

    @pyqtProperty(int)
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, new_texture):
        self._texture = new_texture

    def texture_change(self, state):
        if state:
            self.texture = POLISHED

        else:
            self.texture = MATTE

        self.set_pixmap()


    def set_pixmap(self):
        """Updates the selected brush and sets the drawn pixmap."""
        self.brush = brush_factory(self.base_button.selected_color,
                                   self.highlight_button.selected_color,
                                   self.texture)

        # Prepares the pixmap surface
        pixmap = QPixmap(28, 40)
        pixmap.fill(QColor(0, 0, 0, 0))

        # Paint on the pixmap
        bead_painter.begin(pixmap)

        bead_painter.setPen(QColor(170, 170, 168))
        bead_painter.setBrush(self.brush)
        bead_painter.drawRoundedRect(0, 0, 27, 39, 5, 5)

        bead_painter.end()

        # Update class members
        self.brush_changed.emit()
        self.pixmap_item.setPixmap(pixmap)
        self.pixmap_item.update()
