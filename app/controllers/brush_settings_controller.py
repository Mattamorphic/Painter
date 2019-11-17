'''
    Brush Settings Controller

    Author:
        Matt Barber <mfmbarber@gmail.com>
'''
from .base_controller import BaseController
from app.views.components.brush_settings import (
    BrushCapOptions, BrushColourPicker, BrushJoinOptions, BrushLineOptions,
    BrushTypeOptions, BrushPreview, BrushSizeSlider)
from app.views.layouts import BrushSettingsLayout
from PyQt5.QtCore import pyqtSignal


class BrushSettingsController(BaseController):
    '''
        The controller for all the components that modify the settings on
        the brush model

        Args:
            brush (Brush): brush
    '''
    update = pyqtSignal(object)

    def __init__(self, brush, parent=None):
        super().__init__(parent)
        self.brush = brush
        # Add controlled components
        self.initializeComponents()
        # Insert the components into a layout (a view)
        self.setLayout(
            BrushSettingsLayout(
                {
                    'Brush Settings': {
                        'Type': self.getComponentWidget('type'),
                        'Cap': self.getComponentWidget('cap'),
                        'Line': self.getComponentWidget('lines'),
                        'Join': self.getComponentWidget('joins')
                    }
                }, {'Brush Size': {
                    '': self.getComponentWidget('size')
                }}, {
                    'Brush Preview': {
                        None: [
                            self.getComponentWidget('colour'),
                            self.getComponentWidget('preview')
                        ],
                    }
                }))

    def initializeComponents(self):
        '''
            Initialize the components for this controller
        '''

        self.addComponents({
            "size":
            self.makeComponent(
                BrushSizeSlider(self.brush.getSize()),
                lambda v: self.updateBrush(v, self.brush.setSize)),
            "type":
            self.makeComponent(
                BrushTypeOptions(self.brush.getAllBrushTypes()),
                lambda v: self.updateBrush(v, self.brush.setBrushType)),
            "cap":
            self.makeComponent(
                BrushCapOptions(self.brush.getAllCapTypes()),
                lambda v: self.updateBrush(v, self.brush.setCapType)),
            "joins":
            self.makeComponent(
                BrushJoinOptions(self.brush.getAllJoinTypes()),
                lambda v: self.updateBrush(v, self.brush.setJoinType)),
            "lines":
            self.makeComponent(
                BrushLineOptions(self.brush.getAllLineTypes()),
                lambda v: self.updateBrush(v, self.brush.setLineType)),
            "colour":
            self.makeComponent(
                BrushColourPicker(self.brush.getColour(), self),
                lambda v: self.updateBrush(v, self.brush.setColour)),
            "preview":
            self.makeComponent(BrushPreview(self.brush))
        })

    def updateBrush(self, value, callback):
        '''
            Any updates to the brush have to update the preview

            Args:
                value (mixed):  The value being updated on the brush
                callback (func): A method on the brush
        '''
        callback(value)
        self.updatePreview()

    def updatePreview(self):
        '''
            Redraw the preview component
        '''
        preview = self.getComponentWidget('preview')
        if not preview:
            raise RuntimeError("Preview component not set")
        preview.drawPreview(self.brush)

    def resizeEvent(self, _):
        '''
            On widget resize, redraw the preview
        '''
        self.updatePreview()

    def showEvent(self, _):
        '''
            On show event, redraw the preview
        '''
        self.updatePreview()
