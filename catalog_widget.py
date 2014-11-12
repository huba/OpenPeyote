from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from util import *



class Catalog(QDockWidget):
    def __init__(self, parent=None):
        super(Catalog, self).__init__(parent)
        self.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        self.setWindowTitle('Catalog')

        self.catalog_tree = QTreeWidget()
        self.catalog_tree.setColumnCount(1)
        self.catalog_tree.setHeaderLabel('Name')
        self.setWidget(self.catalog_tree)

    def add_collection(self, collection):
        self.catalog_tree.addTopLevelItem(collection)

    def current_item(self):
        return self.catalog_tree.currentItem()

    def find_type(self, type_name):
        try:
            # Return the first match
            return self.catalog_tree.findItems(type_name, Qt.MatchRecursive, 0)[0]

        except IndexError:
            # Found nothing
            return None


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
