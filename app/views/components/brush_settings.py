'''
    Brush Settings
    Holds all of the widgets / components that are using to control the brush

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QImage, QPainter
from PyQt5.QtWidgets import (QColorDialog, QComboBox, QLabel, QPushButton,
                             QSizePolicy, QSlider, QWidget)

from app.views.layouts import BrushSizeLayout


class BrushPreview(QWidget):
    '''
        Display a preview of the brush

        Args:
            brush (Brush): The brush
    '''
    def __init__(self, brush):
        super().__init__()
        self.setMinimumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.brush = brush
        self.previewBackgroundColour = Qt.white
        self.clear()
        self.drawPreview(brush)

    def drawPreview(self, brush):
        '''
            Draw a preview, based on the current type of brush

            Args:
                brush
        '''
        if brush.getBrushType() == Constants.BrushTypes.BRUSH:
            self.drawBrushPreview(brush)
        if brush.getBrushType() == Constants.BrushTypes.LINE:
            self.drawLinePreview(brush)

    def drawLinePreview(self, brush):
        '''
            Draw the preview on the widget

            brush (Brush): The brush
        '''
        self.brush = brush
        mid = self.rect().height() // 2
        self.clear()
        painter = QPainter(self.image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self.brush.getPen())
        painter.drawLine(0, mid, self.rect().width(), mid)
        super().update()

    def drawBrushPreview(self, brush):
        '''
            Draw the preview on the widget

            brush (Brush): The brush
        '''
        self.brush = brush
        self.clear()
        painter = QPainter(self.image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self.brush.getPen())
        painter.drawPoint(self.rect().center())
        super().update()

    def paintEvent(self, event=None):
        '''
            Paint event handler
        '''
        canvasPainter = QPainter(self)
        canvasPainter.setRenderHint(QPainter.Antialiasing, True)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def setBackgroundColour(self, colour):
        '''
            Background colour handler
        '''
        self.previewBackgroundColour = colour
        self.drawPreview(self.brush)

    def clear(self):
        '''
            Clear the preview
        '''
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(self.previewBackgroundColour)


class BrushOptions(QComboBox):
    '''
        Brush options base class

        Args:
            options (dict): The options
    '''
    onChange = pyqtSignal(str)

    def __init__(self, options={}, parent=None):
        super().__init__()
        self.options = list(options.keys())
        for item in self.options:
            if Constants.Icons.hasKey(item):
                self.addItem(QIcon(Constants.Icons[item].value),
                             item.capitalize())
            else:
                self.addItem(item.capitalize())
        self.currentIndexChanged.connect(self.optionIndexChanged)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def optionIndexChanged(self, index: int):
        '''
            When the index changes, find the value for that index and emit

            Args:
                index (int): The selected index
        '''
        if self.options and self.options[index]:
            self.onChange.emit(self.options[index])


class BrushCapOptions(BrushOptions):
    '''
        A child instance of brush options for cap
    '''
    def __init__(self, caps={}, parent=None):
        super().__init__(caps, parent)


class BrushJoinOptions(BrushOptions):
    '''
        A child instance of brush options for join
    '''
    def __init__(self, joins={}, parent=None):
        super().__init__(joins, parent)


class BrushLineOptions(BrushOptions):
    '''
        A child instance of brush options for line
    '''
    def __init__(self, lines={}, parent=None):
        super().__init__(lines, parent)


class BrushTypeOptions(BrushOptions):
    '''
        A child instance of brush options for type
    '''
    def __init__(self, types={}, parent=None):
        super().__init__(types, parent)


class BrushSizeSlider(QWidget):
    '''
        A slider for changing the brush size

        Args:
            size (int): The size of the brush
    '''

    onChange = pyqtSignal(int)

    def __init__(self, size: int):
        super().__init__()
        self.label = QLabel(str(size) + "px")
        self.slider = QSlider()
        self.slider.setValue(size)
        self.slider.valueChanged.connect(self.updateSize)
        self.setLayout(BrushSizeLayout(self.label, self.slider))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def updateSize(self, value: int):
        '''
            On size change, update the slider value

            Args:
                value (int): The value of the slider
        '''
        self.label.setText(str(value) + "px")
        self.onChange.emit(value)


class BrushColourPicker(QPushButton):
    '''
        A Colour picker, triggered by push button

        Args:
            colour (QColor): The initial colour

    '''
    onChange = pyqtSignal(object)

    def __init__(self, colour, parent=None):
        super().__init__(QIcon(Constants.Icons.PALETTE.value), 'Palette',
                         parent)
        self.parent = parent
        self.colour = colour
        self.clicked.connect(self.openColourDialog)

    def openColourDialog(self):
        '''
            Execute the colour dialog
        '''
        dialog = QColorDialog(self.colour, self.parent)
        dialog.currentColorChanged.connect(self.onChange.emit)
        dialog.exec_()
