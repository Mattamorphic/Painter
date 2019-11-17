'''
    Canvas settings
    Widgets / components for managing the canvas

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QColorDialog, QPushButton)


class CanvasColourPicker(QPushButton):
    '''
        Open a canvas background colour selector on button press

        Args:
            colour (QColor): The initial colour for the picker
    '''
    onChange = pyqtSignal(object)

    def __init__(self, colour, parent=None):
        super().__init__('Fill colour', parent)
        self.parent = parent
        self.colour = colour
        self.clicked.connect(self.openColourDialog)

    def openColourDialog(self):
        '''
            On click, open the dialog
        '''
        dialog = QColorDialog(self.colour, self.parent)
        dialog.currentColorChanged.connect(self.onChange.emit)
        dialog.exec_()
