'''
    Canvas Controller

    Author:
        Matt Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from .base_controller import BaseController
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter


class CanvasController(BaseController):
    '''
        Canvas Controller

        Args:
            brush (Brush): brush
    '''
    update = pyqtSignal(object)

    def __init__(self, canvas, brush, parent):
        super().__init__(parent)    # TODO add a signal for a paint event
        self.setMinimumSize(400, 400)
        self.brush = brush
        self.canvas = canvas

    def clear(self):
        self.canvas.clear()
        super().update()

    def undo(self):
        self.canvas.undo()
        super().update()

    def isBrush(self):
        '''
            A helper check for if the brush is currently a brush

            Returns:
                (bool)
        '''
        return self.brush.getBrushType() == Constants.BrushTypes.BRUSH

    def isLine(self):
        '''
            A helper check for if the brush is currently a line

            Returns:
                (bool)
        '''
        return self.brush.getBrushType() == Constants.BrushTypes.LINE

    def mousePressEvent(self, event):
        '''
            Handle a mouse press event
        '''
        if event.button() == Qt.LeftButton:
            # On click preserve the current image
            self.canvas.snapshotImage()
            self.canvas.brushOnCanvas(event.pos())
            if self.isBrush():
                self.canvas.draw(event.pos(), self.brush)
            super().update()
            self.update.emit(self.canvas.state)

    def mouseMoveEvent(self, event):
        '''
            Handle a mouse move event
        '''
        if event.buttons() and Qt.LeftButton and self.canvas.isDrawing():
            if self.isBrush():
                self.canvas.draw(event.pos(), self.brush)
            if self.isLine():
                self.canvas.drawPreview(event.pos(), self.brush)
            super().update()
            self.update.emit(self.canvas.state)

    def mouseReleaseEvent(self, event):
        '''
            Handle a mouse release event
        '''
        if event.button() == Qt.LeftButton:
            if self.isLine():
                self.canvas.drawActual(event.pos(), self.brush)
                super().update()
            self.canvas.brushAwayFromCanvas()
            self.update.emit(self.canvas.state)

    def paintEvent(self, event):
        '''
            Handle a paint event
        '''
        # Draws the rectangular portion source of the given image into the
        # target rectangle in the paint device.
        QPainter(self).drawImage(self.rect(), self.canvas.image,
                                 self.canvas.image.rect())
        super().update()

    def resizeEvent(self, _):
        '''
            On resize, reset the image
        '''
        self.canvas.setSize(self.size())
        self.canvas.reset()
        super().update()

    def showEvent(self, _):
        '''
            On show, reset the image
        '''
        self.canvas.reset()
        super().update()
