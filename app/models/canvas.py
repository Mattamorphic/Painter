'''
    Canvas Model
    A model for representing the canvas
'''
from .state import State
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage, QPainter


class Canvas:
    '''
        The canvas

        Args:
            size (QSize): The size of the canvas
    '''
    previous = []
    isSaved = False

    class CanvasState(State):
        '''
            Canvas State
        '''
        isDrawing = False
        hasPreview = False
        initialPoint = QPoint()
        lastPoint = QPoint()

        def printState(self):
            if self.isDrawing:
                if self.hasPreview:
                    return (
                        "Drawing a preview from " +
                        f"{self.initialPoint.x()}, {self.initialPoint.y()} to"
                        + f"{self.lastPoint.x()}, {self.lastPoint.y()}")
                else:
                    return f"Drawing at {self.lastPoint.x()}, {self.lastPoint.y()}"
            else:
                return "Ready..."

    def __init__(self, size):
        self.size = size
        self.state = self.CanvasState()
        self.clear()

    def __drawing__(self, fromPoint, toPoint, pen):
        '''
            Method for drawing on the canvas (private)

            Args:
                fromPoint (QPoint): The start point
                toPoint   (QPoint): The end point
                pen       (QPen):   The pen to draw with
        '''
        self.state.lastPoint = toPoint
        self.isSaved = False
        painter = QPainter(self.image)
        painter.setPen(pen)
        if fromPoint != toPoint:
            painter.drawLine(fromPoint, toPoint)
        else:
            painter.drawPoint(toPoint)

    def undo(self):
        '''
            Return the canvas to a previous state
        '''
        if self.previous:
            self.setImage(self.previous.pop())

    def snapshotImage(self):
        '''
            Snapshot the current state of the canvas
        '''
        self.previous.append(QImage(self.image))
        if len(self.previous) > 50:
            self.previous.pop(0)

    def clear(self):
        '''
            Re-initialize the canvas
        '''
        image = QImage(self.size, QImage.Format_RGB32)
        image.fill(Qt.white)
        self.previous = []
        self.image = image

    def setImage(self, image):
        '''
            Set the canvas to a QImage

            Args:
                image (QImage): The image for the canvas
        '''
        self.image = QImage(image).scaled(self.size, Qt.KeepAspectRatio,
                                          Qt.SmoothTransformation)

    def draw(self, toPoint, brush):
        '''
            General draw method to a point, with a brush

            Args:
                toPoint (QPoint): The point to paint to
                brush   (Brush):  The brush model to use

            Throws:
                RuntimeError : Must set brush on canvas
        '''
        if not self.isDrawing():
            raise RuntimeError("Canvas.brushOnCanvas must be called")
        self.__drawing__(self.state.lastPoint, toPoint, brush.getPen())

    def drawActual(self, toPoint, brush):
        '''
            Draw actual after preview

            Args:
                toPoint (QPoint): The point to paint to
                brush   (Brush):  The brush model to use

            Throws:
                RuntimeError : Must set brush on canvas
        '''
        if not self.isDrawing():
            raise RuntimeError("Canvas.brushOnCanvas must be called")
        if self.state.hasPreview:
            self.undo()
            self.state.hasPreview = False
        self.__drawing__(self.state.initialPoint, toPoint, brush.getPen())

    def drawPreview(self, toPoint, brush):
        '''
            Draw a preview to a point, with a brush

            Args:
                toPoint (QPoint): The point to paint to
                brush   (Brush):  The brush model to use

            Throws:
                RuntimeError : Must set brush on canvas
        '''
        if not self.isDrawing():
            raise RuntimeError("Canvas.brushOnCanvas must be called")
        if self.state.hasPreview:
            self.undo()
            self.state.hasPreview = False
        self.snapshotImage()
        self.__drawing__(self.state.initialPoint, toPoint,
                         brush.getPreviewPen())
        self.state.hasPreview = True

    def getImage(self):
        '''
            Get the QImage attribute

            Returns:
                (QImage)
        '''
        return self.image

    def save(self, path):
        '''
            Save the QImage to a file

            Args:
                path (str): Path to save to
        '''
        # TODO: Throw is path doesn't exist / isn't writable
        self.image.save(path)
        self.isSaved = True

    def isEdited(self):
        '''
            Check to see if there are edits

            Returns:
                (bool)
        '''
        return True if self.previous else False

    def isSaved(self):
        '''
            Check to see if the changes have been saved

            Returns:
                (bool)
        '''
        return self.isSaved

    def isDrawing(self):
        '''
            Check to see if the canvas is being drawn on

            Returns:
                (bool)
        '''
        return self.state.isDrawing

    def brushOnCanvas(self, point):
        '''
            Set a brush on the canvas at the given point

            Args:
                point (QPoint): The touch point
        '''
        self.state.isDrawing = True
        self.state.initialPoint = point
        self.state.lastPoint = point

    def brushAwayFromCanvas(self):
        '''
            Remove a brush from the canvas
        '''
        self.state.isDrawing = False
        self.state.initialPoint = None
        self.state.lastPoint = None

    def reset(self):
        '''
            Reset the image using the current image
        '''
        self.setImage(self.image)

    def setSize(self, size):
        '''
            Set the size of the canvas

            Args:
                size (QSize): The size to use for the canvas
        '''
        self.size = size
