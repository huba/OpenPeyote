from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from util import *
from wizards_and_dialogs import *

import json



class Catalog(QTreeWidget):
    def __init__(self, parent=None):
        super(Catalog, self).__init__(parent)
        self.setWindowTitle('Catalog')

        self.setColumnCount(2)
        self.setHeaderLabels(['Name', 'Catalog Number'])

    def add_collection(self, collection):
        self.addTopLevelItem(collection)

    def current_item(self):
        return self.currentItem()

    def find_type(self, type_catalog_id):
        try:
            # Return the first match
            return self.findItems(type_catalog_id, Qt.MatchRecursive, 1)[0]

        except IndexError:
            # Found nothing
            return None

    def contextMenuEvent(self, evt):
        """Creates and shows a context menu."""

        if self.itemAt(evt.pos()):
            self._collection_context(evt)

        else:
            self._root_context(evt)

        evt.accept()

    def _collection_context(self, evt):
        if self.itemAt(evt.pos()).type() != 1000:
            return

        popup = QMenu()

        new_bead_action = popup.addAction('Add New Bead')
        new_bead_action.triggered.connect(self.add_bead_slot)

        export_collection_action = popup.addAction('Export Collection')
        export_collection_action.triggered.connect(self.export_collection)

        popup.exec_(evt.globalPos())


    def _root_context(self, evt):
        popup = QMenu()

        new_collection_action = popup.addAction('Add New Collection')
        new_collection_action.triggered.connect(self.add_collection_slot)

        import_collection_action = popup.addAction('Import Collection')
        import_collection_action.triggered.connect(self.import_collections)

        popup.exec_(evt.globalPos())


    def add_collection_slot(self):
        """Slot for calling a nw collection wizard."""
        wizard = CollectionWizard(self)
        wizard.exec_()


    def add_bead_slot(self):
        """Slot for calling a new bead wizard."""
        # Assume that the right clicked item is a collection.
        wizard = BeadWizard(self.currentItem())
        wizard.exec_()


    def export_collection(self):
        collection = self.currentItem()
        name_s = '_'.join(collection.data(0,  Qt.DisplayRole).lower().split(' '))
        (path, flt) = QFileDialog.getSaveFileName(self, 'Export Collection',
                                                  './{}{}'.format(name_s, collection_extension),
                                                  'Bead Collection (*{})'.format(collection_extension))

        if flt == '':
            # They clicked cancel.
            return

        with open(path, 'w') as file:
            json.dump(collection.to_dict(), file)


    def import_collections(self):
        (paths, flt) = QFileDialog.getOpenFileNames(parent=self, caption='Import Collection',
                                                    filter='Bead Collection (*{})'.format(collection_extension))

        if flt == '':
            return

        for path in paths:
            self.import_collection(path)


    def import_collection(self, path):
        with open(path, 'r') as file:
            rdict = json.load(file)
            name = rdict['__name__']
            bt_list = rdict['__bead_types__']

            new_collection = Collection(name)

            for bt in bt_list:
                name = bt['__name__']
                catalog_number = bt['__catalog_number__']
                base_color = bt['__base_color__']
                highlight_color = bt['__highlight_color__']
                texture = bt['__texture__']

                brush = brush_factory(QColor(base_color), QColor(highlight_color), texture)

                new_bead_type = BeadType(name, catalog_number, brush, base_color, highlight_color, texture)

                new_collection.addChild(new_bead_type)

            self.add_collection(new_collection)



class Collection(QTreeWidgetItem):
    def __init__(self, name):
        super(Collection, self).__init__(1000)
        self.setData(0, Qt.DisplayRole, QVariant(name))
        self.bead_types = []


    def addChild(self, child):
        """Only add child if it's a bead type instance..."""
        if child.type() == 1001:
            self.bead_types.append(child)
            super(Collection, self).addChild(child)


    def to_dict(self):
        rdict = {}
        rdict['__name__'] = self.data(0,  Qt.DisplayRole)
        rdict['__bead_types__'] = []

        for bead_type in self.bead_types:
            rdict['__bead_types__'].append(bead_type.to_dict())

        return rdict



class BeadType(QTreeWidgetItem):
    def __init__(self, name, catalog_number, brush, base_color, highlight_color, texture):
        super(BeadType, self).__init__(1001)
        self.setData(0, Qt.DisplayRole, QVariant(name))
        self.setData(1, Qt.DisplayRole, QVariant(catalog_number))
        self.base_color, self.highlight_color, self.catalog_number = base_color, highlight_color, catalog_number
        self.texture = texture
        self.set_pixmap(brush)


    def addChild(self, child):
        """Contraception hahaha! It prevents adding child nodes."""
        return


    def to_dict(self):
        rdict = {}
        rdict['__name__'] = self.data(0, Qt.DisplayRole)
        rdict['__catalog_number__'] = self.data(1, Qt.DisplayRole)
        rdict['__base_color__'] = self.base_color
        rdict['__highlight_color__'] = self.highlight_color
        rdict['__texture__'] = self.texture
        return rdict


    def set_pixmap(self, brush):
        global bead_painter
        # NOTE: This is hard coded here, but not elswhere
        self.pixmap = QPixmap(28, 40)
        self.pixmap.fill(QColor(0, 0, 0, 0))

        # paint the icon...
        bead_painter.begin(self.pixmap)

        bead_painter.setPen(QColor(170, 170, 168))
        bead_painter.setBrush(brush)
        # TODO: shape this nicer.
        bead_painter.drawRoundedRect(0, 0, 27, 39, 5, 5)

        bead_painter.end()

        self.setIcon(0, QIcon(self.pixmap))
