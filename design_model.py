"""
This module takes care of the components of the design iteslf.
Author: Huba Z. Nagy (12huba@gmail.com)
Date: 10.11.2014
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from design_visual_guide import *
from util import *



class DesignScene(QGraphicsScene):
    """This class holds the data for the peyote design, it integrates
    with Qt's GraphicsView framework."""
    def __init__(self, parent=None, name='(Untitled)', track_width=5, tracks=10, height=40):
        """Sets up the neccessary parameters for generating the model, at
        the moment it only generates a blank design."""
        # TODO: add load/save functionality

        super(DesignScene, self).__init__(parent)

        self.track_width, self.name = track_width, name
        self.dimensions = (tracks * track_width, height)

        Bead.set_track_width(track_width)
        self.grid = Grid(Bead, self.dimensions)
        self.addItem(self.grid)

        self._beads = []
        self.populate()


    def populate(self):
        """Generates the blank design to the specified dimensions."""
        for row in range(0, self.dimensions[HEIGHT]):
            row_list = []
            for col in range(0, self.dimensions[WIDTH]):
                new_bead = Bead(location=(col, row))
                row_list.append(new_bead)
                self.addItem(new_bead)

            self._beads.append(row_list)



class Bead(QGraphicsItem):
    """A class for representing the individual beads of the peyote design, it integrates
    with Qt's GraphicsView framework."""
    dimension = (28, 40)
    margain = 4
    _rounding = 5
    track_width = 3
    _default_brush = QBrush(QColor(230, 230, 228))

    def __init__(self, parent=None, location=(0, 0), color=None):
        """Standard python __init__ function, should not need too much explaining."""
        super(Bead, self).__init__(parent)
        self.setAcceptedMouseButtons(Qt.LeftButton)

        self._location = location
        self._color = color

        self._calc_pos()

    def _calc_pos(self):
        """Sets up the bead's pxel coordinates relative to the scene."""
        if (self._location[X] // self.track_width % 2):
            adjustment = self.dimension[HEIGHT] // 2

        else:
            adjustment = 0

        self.setPos((self._location[X] * (self.dimension[WIDTH] + self.margain)) + self.margain,
                    (self._location[Y] * (self.dimension[HEIGHT] + self.margain)) + self.margain + adjustment)

    @classmethod
    def set_track_width(cls, new_track_width):
        """Don't call this once you initialized any instances of the class it will
        mess things up. Be warned!"""
        cls.track_width = new_track_width


    def boundingRect(self):
        """QGraphicsItem's required boundingRect function used for all sorts of sorcery."""
        return QRectF(0, 0, self.dimension[WIDTH], self.dimension[HEIGHT])


    def paint(self, painter, option, widget):
        """A really artsy function... It draws. See QGraphicsItem's documentation for more"""
        painter.setPen(QColor(170, 170, 168))
        if self._color:
            painter.setBrush(self._color)

        else:
            painter.setBrush(self._default_brush)

        painter.drawRoundedRect(0, 0, self.dimension[WIDTH], self.dimension[HEIGHT], self._rounding, self._rounding)


    def mousePressEvent(self, evt):
        """Handles mouse events."""
        # TODO: this is only for testing, implement this with user defined colors...
        if self._color:
            self._color = None

        else:
            self._color = Qt.cyan

        # Must run update to redraw...
        self.update()
