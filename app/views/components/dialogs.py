'''
    Dialogs

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap


class BaseDialog(QDialog):
    '''
        A helper class for creating dialogs

        Args:
            parent (class): The owner of this dialog
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.heading = QLabel()
        self.subHeading = QLabel()
        self.content = QLabel()
        self.content.setSizePolicy(QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        self.buttonBox = QDialogButtonBox()
        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.subHeading)
        layout.addWidget(self.content)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

    def addButton(self, text: str, role, callback=None):
        '''
            Add a button with text, a role, and an optional callback

            Args:
                text (str):      The text for the button
                role (enum):     An option from the wrapper enum Constants.DialogButtonRoles
                callback (func): An optional callback to tie to the button
        '''

        if role not in Constants.DialogButtonRoles:
            raise ValueError('Role must be one of Constants.DialogButtonRoles')

        btn = self.buttonBox.addButton(text, role.value)
        if callback:
            btn.clicked.connect(callback)

    def setHeading(self, text: str):
        '''
            Setter method for the heading label

            Args:
                text (str): Text for the main label
        '''
        self.heading.setText(text)

    def setSubHeading(self, text: str):
        '''
            Setter method for the subheading label

            Args:
                text (str): Text for the sub label
        '''
        self.subHeading.setText(text)

    def setContent(self, content):
        if isinstance(content, str):
            self.content.setText(str)
        elif isinstance(content, QPixmap):
            self.content.setPixmap(content)

    def setTitle(self, text: str):
        '''
            Setter method for the dialog title

            Args:
                text (str): Text for the window title
        '''
        self.setWindowTitle(text)

    def onAccept(self, callback):
        '''
            Human friendly wrapper for the button box accepted signal

            Args:
                callback (func): Slot to call
        '''
        self.buttonBox.accepted.connect(callback)

    def onReject(self, callback):
        '''
            Human friendly wrapper for the button box regjected signal

            Args:
                callback (func): Slot to call
        '''
        self.buttonBox.rejected.connect(callback)


class AboutDialog(BaseDialog):
    '''
        About PyPainter dialog
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeading('PyPainter')
        self.setSubHeading('A PyPainter by Matt Barber')
        self.setContent(QPixmap(Constants.IMAGES_LOCATION + "logo.png"))
        self.setTitle("About PyPainter")
        self.addButton('OK', Constants.DialogButtonRoles.ACCEPT)
        self.onAccept(self.close)


class QuitDialog(BaseDialog):
    '''
        Dialog for handling quit

        Args:
            save (func): Callback for handling saving
    '''
    def __init__(self, save=None, parent=None):
        super().__init__(parent)
        self.setHeading('Quit PyPainter?')
        self.save = save
        self.initUnsaved() if save is not None else self.initQuit()

    def initUnsaved(self):
        '''
            If there is a save callback, there is unsaved changes
        '''
        self.setSubHeading('Unsaved changes, do you want to save first')
        self.addButton('Save', Constants.DialogButtonRoles.YES)
        self.addButton('Cancel', Constants.DialogButtonRoles.NO)
        self.addButton('Don\'t Save', Constants.DialogButtonRoles.DESTRUCTIVE,
                       self.quit)
        self.onAccept(lambda: (self.save(), self.quit()))
        self.onReject(self.close)

    def initQuit(self):
        '''
            If there is not a save callback, then don't ask the user to save
        '''
        self.setSubHeading('Are you sure you want to quit?')
        self.addButton('Quit', Constants.DialogButtonRoles.YES)
        self.addButton('Cancel', Constants.DialogButtonRoles.NO)
        self.onAccept(self.quit)
        self.onReject(self.close)

    def quit(self):
        '''
            A helper method to wrap the instance quitting
        '''
        QCoreApplication.instance().quit()
