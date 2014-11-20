"""
This module houses visual guides like the grid.
Author: Huba Z. Nagy (12huba@gmail.com)
Date: 11.11.2014
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from util import *



class Grid(QGraphicsItem):
    """QGraphicsItem that draws a simple grid on top of the design to make it
    visually easier to navigate."""
    def __init__(self, track_width, dimensions, parent=None):
        """Pretty straigt forward __init__ function. Nothing fancy."""
        super(Grid, self).__init__(parent)
        self.track_width, self.dimension = track_width, dimensions
        self.pixel_dimensions = (28, 40)
        self.margain = 4

    def boundingRect(self):
        """QGraphicsItem's required bounding rect function, used for culling offscreen geometry
        and similar magical things."""
        return QRectF(-30, -30,
                      (self.pixel_dimensions[WIDTH] + self.margain) * self.dimension[WIDTH] + 60,
                      (self.pixel_dimensions[HEIGHT] + self.margain) * self.dimension[HEIGHT] + 60)

    def paint(self, painter, option, widget):
        """Overloading the paint function of QGraphicsItem all the drawing is done here."""
        # Set up painter with the right colors width etc.
        painter.setPen(QPen(QBrush(QColor(140, 139, 134)), 2.5))

        # Calculate some basic common values
        track_pixel_width =  self.track_width * (self.margain + self.pixel_dimensions[WIDTH])
        bottom = (self.pixel_dimensions[HEIGHT] + self.margain) * self.dimension[HEIGHT] + self.pixel_dimensions[HEIGHT] // 2
        right = (self.pixel_dimensions[WIDTH] + self.margain) * self.dimension[WIDTH]

        # Draw vertical lines
        for vertical in range(0, self.dimension[WIDTH] // self.track_width + 1):
            # Calculate the base x coordinate
            xc = vertical * (track_pixel_width) + self.margain // 2

            # Draw the vertical line
            painter.drawLine(xc, - 30, xc, bottom + 30)


        # Draw horizontal lines
        for horizontal in range(0, self.dimension[1] // 5 + 1):
            # Calculate the base y coordinate
            yc = 5 * horizontal * (self.pixel_dimensions[HEIGHT] + self.margain) + self.margain // 2

            for track in range(0, self.dimension[WIDTH] // self.track_width):
                # Shift down for every second track
                if track % 2 == 1:
                    adjustement = self.pixel_dimensions[HEIGHT] // 2

                else:
                    adjustement = 0

                # Extend 30 px before the start
                if track == 0:
                    h_adjustement = - 30

                else:
                    h_adjustement = 0

                # Extend 30 px after the end
                if track == (self.dimension[WIDTH] // self.track_width - 1):
                    w_adjustement = 30

                else:
                    w_adjustement = 0

                # Draw the horizontal line
                painter.drawLine(track * track_pixel_width + self.margain // 2 + h_adjustement,
                                 yc + adjustement,
                                 (track + 1) * track_pixel_width + self.margain // 2 + w_adjustement,
                                 yc + adjustement)
