import PySide2
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsView, QMenu, QAction


class MainGraphicsWidget(QGraphicsView):
    unselect_contracts = QtCore.Signal(name="unselect_contracts")

    def __init__(self, parent=None):
        super(MainGraphicsWidget, self).__init__(parent)
        # sceneRect is a property of QGraphicsView and  should not be overwritten
        # self.sceneRect = self._scene.sceneRect()
        self.startPos = None

    def mousePressEvent(self, event):
        self.unselect_contracts.emit()

        if event.modifiers() & Qt.ShiftModifier and event.button() == Qt.LeftButton:
            # store the origin point
            self.startPos = event.pos()
        else:
            super(MainGraphicsWidget, self).mousePressEvent(event)

    def wheelEvent(self, event: PySide2.QtGui.QWheelEvent) -> None:
        if event.modifiers() & Qt.ShiftModifier:
            #prevent from unwanted movement/ side effects
            return

        super().wheelEvent(event)

    def mouseMoveEvent(self, event):
        if self.startPos is not None:
            # compute the difference between the current cursor position and the
            # previous saved origin point
            delta = self.startPos - event.pos()
            # get the current transformation (which is a matrix that includes the
            # scaling ratios
            transform = self.transform()
            # m11 refers to the horizontal scale, m22 to the vertical scale;
            # divide the delta by their corresponding ratio
            deltaX = delta.x() / transform.m11()
            deltaY = delta.y() / transform.m22()
            # translate the current sceneRect by the delta
            self.setSceneRect(self.sceneRect().translated(deltaX, deltaY))
            # update the new origin point to the current position
            self.startPos = event.pos()
        else:
            super(MainGraphicsWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.startPos = None
        super(MainGraphicsWidget, self).mouseReleaseEvent(event)
