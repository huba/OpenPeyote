"""
This module houses the QGraphicsView widget that can display the design.
Author: Huba Z. Nagy (12huba@gmail.com)
Date: 10.11.2014
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *
from PyQt5.QtGui import *

from design_model import *



class PatternArea(QGraphicsView):
    _minzoom = 0.3
    _maxzoom = 2.0
    def __init__(self, design=None, parent=None):
        super(PatternArea, self).__init__(parent)
        self.setViewport(QGLWidget())
        self.setRenderHint(QPainter.Antialiasing, False)
        self.setBackgroundBrush(QBrush(QColor(190, 189, 184)))
        self._zoom = 1
        self._panning = False
        self._previous_pos = None
        self.filepath = None

        if not design:
            design = DesignScene(self)

        self.setWindowTitle(design.name)
        self.setScene(design)
        self.setInteractive(True)

    def zoom(self, delta):
        if self._zoom == self._maxzoom and delta > 0:
            return

        self._zoom += delta

        if self._zoom < self._minzoom:
            self._zoom = self._minzoom

        elif self._zoom > self._maxzoom:
            self._zoom = self._maxzoom

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.resetTransform()
        self.scale(self._zoom, self._zoom)

    def wheelEvent(self, evt):
        """Deals with the mousewheel, calls the zoom function accordingly."""
        if evt.angleDelta().y() > 0:
            self.zoom(0.1)

        else:
            self.zoom(-0.1)

        evt.accept()

    def mousePressEvent(self, evt):
        if evt.button() == Qt.RightButton:
            self._panning = True
            self._previous_pos = evt.pos()
            evt.accept()

        else:
            super(PatternArea, self).mousePressEvent(evt)
            evt.ignore()

    def mouseReleaseEvent(self, evt):
        if evt.button() == Qt.RightButton:
            self._panning = False
            evt.accept()

        else:
            super(PatternArea, self).mouseReleaseEvent(evt)
            evt.ignore()

    def mouseMoveEvent(self, evt):
        if self._panning:
            delta = self.mapFromParent(evt.pos()) - self.mapFromParent(self._previous_pos)
            self.translate(delta.x(), delta.y())
            self._previous_pos = evt.pos()

        else:
            super(PatternArea, self).mouseMoveEvent(evt)
