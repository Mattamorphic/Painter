'''
    App
    Core app container for the painter

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.controllers.main_controller import MainController
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDesktopWidget, QMainWindow, QMenuBar)


class Painter(QMainWindow):
    '''
        Main window for the Painter app
    '''
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''
            Initializes the Painter UI
        '''
        self.center()
        self.setWindowTitle("Painter")
        self.setWindowIcon(QIcon('../view/assets/icons/paint-brush.png'))
        self.updateStatusBar("Starting Up...")
        # Now launch main
        self.initMain()
        self.initMenu()
        self.show()

    def initMain(self):
        '''
            Initializes the main  controller and attaches the widget (as a view)
        '''
        self.updateStatusBar("Ready...")
        self.mainController = MainController()
        self.mainController.update.connect(self.stateUpdate)
        self.setCentralWidget(self.mainController)

    def initMenu(self):
        mainMenu = QMenuBar(self)
        mainMenu.setNativeMenuBar(False)    # Use PyQt Menu over system menu
        self.addSubMenu("&File", mainMenu, self.mainController.getClearAction,
                        self.mainController.getOpenAction,
                        self.mainController.getSaveAction, None,
                        self.mainController.getQuitAction)
        self.addSubMenu("&Edit", mainMenu, self.mainController.getUndoAction)
        self.addSubMenu("&Help", mainMenu, self.mainController.getAboutAction)
        self.setMenuBar(mainMenu)

    def addSubMenu(self, name, parentMenu, *actions):
        subMenu = parentMenu.addMenu(name)
        for action in actions:
            subMenu.addAction(
                action(self)) if action else subMenu.addSeparator()

    def updateStatusBar(self, value):
        '''
            Sets the default value for the status bar
        '''
        self.statusBar().showMessage(value)

    def center(self):
        '''
            Center the GUI on this display
        '''
        # Geometry of the widget relative to its parent
        window_rectangle = self.frameGeometry()
        # Find the display center point
        center_point = QDesktopWidget().availableGeometry().center()
        # Move the geometry
        window_rectangle.moveCenter(center_point)
        self.move(window_rectangle.topLeft())

    def stateUpdate(self, state):
        '''
            Handle state updates

            Args:
                state (State): The state
        '''
        self.updateStatusBar(str(state))
