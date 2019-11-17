'''
    Main Controller
    Controller for the main controls / functions

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from app.models.brush import Brush
from app.models.canvas import Canvas
from app.views.components.dialogs import AboutDialog, QuitDialog
from app.views.layouts import MainLayout
from .brush_settings_controller import BrushSettingsController
from .canvas_controller import CanvasController
from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QWidget


class MainController(QWidget):
    update = pyqtSignal(object)
    '''
        Painter Main Controller
    '''
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 600)
        self.brush = Brush()
        self.canvas = Canvas(QSize(600, 400))
        self.controllers = {}
        self.initControllers()

    def initControllers(self):
        '''
            Initializes the controllers that the MainController relies on
        '''
        self.addController('canvas',
                           CanvasController(self.canvas, self.brush, self),
                           self.canvasUpdate)
        self.addController('brush_settings',
                           BrushSettingsController(self.brush, self),
                           self.brushSettingsUpdate)

        self.setLayout(
            MainLayout(self.getController('canvas'),
                       self.getController('brush_settings')))

    def getAboutAction(self, parent):
        '''
            About Action for the applicaiton menu

            Args:
                parent (class): Owner of the action

            Returns:
                (QAction)
        '''
        return self.createAction(QIcon(Constants.Icons.FOX.value), "About",
                                 lambda: AboutDialog().exec_(), None, parent)

    def getClearAction(self, parent):
        '''
            Clear is effectively new, and reset the canvas

            Args:
                parent (class): Owner of the action

            Returns:
                (QAction)
        '''
        return self.createAction(QIcon(Constants.Icons.NEW.value), "&New",
                                 self.canvas.clear, "Ctrl+N", parent)

    def getOpenAction(self, parent):
        '''
            Open, opens a file dialog, and if there is a valid response it
            attaches this to the canvas

            Args:
                parent (class): Owner of the action

            Returns:
                (QAction)
        '''
        def openImage():
            '''
                Callback for the open action, this triggers the file dialog
                captues the output, and updates thte canvas with this
            '''
            filePath, _ = QFileDialog.getOpenFileName(
                self, "Open Image", "", Constants.ALLOWED_FILE_TYPES)
            if not filePath:
                return
            self.canvas.clear()
            self.canvas.setImage(filePath)

        return self.createAction(QIcon(Constants.Icons.OPEN.value), "&Open",
                                 openImage, "Ctrl+O", parent)

    def getQuitAction(self, parent):

        return self.createAction(
            QIcon(Constants.Icons.EXIT.value), "&Quit",
            lambda: QuitDialog(self.save
                               if self.canvas.isEdited() else None).exec_(),
            "Ctrl+Q", parent)

    def getSaveAction(self, parent):
        '''
            Open, opens a file dialog, and if there is a valid response it
            attaches this to the canvas

            Args:
                parent (class): Owner of the action

            Returns:
                (QAction)
        '''
        return self.createAction(QIcon(Constants.Icons.SAVE.value), "&Save",
                                 self.save, "Ctrl+S", parent)

    def getUndoAction(self, parent):
        return self.createAction(QIcon(Constants.Icons.UNDO.value), "&Undo",
                                 self.canvas.undo, "Ctrl+Z", parent)

    def canvasUpdate(self, state):
        '''

            Args:
                state (CanvasState): The current state of the canvas
        '''
        self.update.emit(state)

    def brushSettingsUpdate(self, state):
        '''
            Args:
                state (BrushState): The current state of the brush
        '''
        self.update.emit(state)

    def addController(self, name, controller, updateCallback):
        '''
            Add a controller

            Args:
                name            (string):           A unique name for the controller
                controller      (BaseController):   A controller to add (instantiated)
                updatetCallback (callable):         A callback for controller update
        '''
        if name in self.controllers:
            raise KeyError("%s already configured" % (name))
        controller.update.connect(updateCallback)
        self.controllers[name] = controller

    def getController(self, name):
        '''
            Get a controller

            Returns:
                (BaseController)
        '''
        return self.controllers[name] if name in self.controllers else None

    def createAction(self,
                     icon,
                     name: str,
                     callback,
                     shortcut=None,
                     parent=None):
        '''
            Helper method to generate a new menu action

            Args:
                name        (str):      A name for the aciton
                callback    (func):     A callback to trigger on action
                shortcut    (str):      A keyboard short cut
                parent      (class):    The owner of this action

            Returns:
                (QAction)
        '''
        action = QAction(icon, name, parent)
        if shortcut:
            action.setShortcut(shortcut)
        action.triggered.connect(callback)
        return action

    def save(self):
        '''
            Callback for the save action, this triggers the file dialog
            captues the current canvas image, writing this to the file path
        '''
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  Constants.ALLOWED_FILE_TYPES)
        if filePath:
            self.canvas.save(filePath)
            return True
        return False
