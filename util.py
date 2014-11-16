"""
Utility module that houses common components.
Author: Huba Z. Nagy (12huba@gmail.com)
Date: 11.11.2014
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

bead_painter = QPainter()

X = WIDTH  = COL = 0
Y = HEIGHT = ROW = 1

design_extension = '.peyd'
collection_extension = '.peyc'

MATTE = 0
POLISHED = 1

def brush_factory(base_color, highlight_color, texture):
    if texture == MATTE:
        # Create gradient to mimic matte surface
        gradient = QLinearGradient(QPointF(14, -30), QPointF(14, 60))
        gradient.setColorAt(0, highlight_color)
        gradient.setColorAt(1, base_color)
        brush = QBrush(gradient)

    elif texture == POLISHED:
        # Creates gradient brush to mimic a shiny surface
        gradient = QLinearGradient(QPointF(14, 0), QPointF(14, 40))
        gradient.setColorAt(0, highlight_color),
        gradient.setColorAt(0.2, highlight_color)
        gradient.setColorAt(0.5, base_color)
        brush = QBrush(gradient)

    else:
        # If the type is unknown it just returns the base color
        brush = QBrush(base_color)

    return brush
