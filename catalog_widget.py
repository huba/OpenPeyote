from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from util import *
from wizards_and_dialogs import *



class Catalog(QTreeWidget):
    def __init__(self, parent=None):
        super(Catalog, self).__init__(parent)
        self.setWindowTitle('Catalog')

        self.setColumnCount(1)
        self.setHeaderLabel('Name')

    def add_collection(self, collection):
        self.addTopLevelItem(collection)

    def current_item(self):
        return self.currentItem()

    def find_type(self, type_name):
        try:
            # Return the first match
            return self.findItems(type_name, Qt.MatchRecursive, 0)[0]

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
        # etc

        popup.exec_(evt.globalPos())


    def _root_context(self, evt):
        popup = QMenu()

        new_collection_action = popup.addAction('Add New Collection')
        new_collection_action.triggered.connect(self.add_collection_slot)

        import_collection_action = popup.addAction('Import Collection')
        # etc

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



class Collection(QTreeWidgetItem):
    def __init__(self, name):
        super(Collection, self).__init__(1000)
        self.setData(0, Qt.DisplayRole, QVariant(name))

    def addChild(self, child):
        """Only add child if it's a bead type instance..."""
        if child.type() == 1001:
            super(Collection, self).addChild(child)



class BeadType(QTreeWidgetItem):
    def __init__(self, name, brush):
        super(BeadType, self).__init__(1001)
        self.setData(0, Qt.DisplayRole, QVariant(name))
        self.set_pixmap(brush)

    def addChild(self, child):
        """Contraception hahaha! It prevents adding child nodes."""
        return

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
