'''
    Constants
    Constants for our classes to use

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtWidgets import QDialogButtonBox, QSizePolicy
from enum import Enum, auto

class Locations(Enum):
    ICONS = "app/views/assets/icons/"
    IMAGES = "app/views/assets/images/"

class Constants:

    ALLOWED_FILE_TYPES = "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)"

    AUTO_WIDTH_AUTO_HEIGHT = (QSizePolicy.Expanding, QSizePolicy.Expanding)
    AUTO_WIDTH_FIXED_HEIGHT = (QSizePolicy.Expanding, QSizePolicy.Fixed)

    IMAGES_LOCATION = Locations.IMAGES.value

    class DialogButtonRoles(Enum):
        '''
            An ENUM to wrap around the DialogButtonRoles
        '''
        ACCEPT = QDialogButtonBox.AcceptRole
        REJECT = QDialogButtonBox.RejectRole
        DESTRUCTIVE = QDialogButtonBox.DestructiveRole
        RESET = QDialogButtonBox.ResetRole
        HELP = QDialogButtonBox.HelpRole
        YES = QDialogButtonBox.YesRole
        NO = QDialogButtonBox.NoRole
        NONE = QDialogButtonBox.NoButton

    class BrushTypes(Enum):
        '''
            An ENUM to wrap around the brush types
        '''
        BRUSH = auto()
        LINE = auto()

    class Icons(Enum):
        BRUSH = Locations.ICONS.value + "brush.png"
        EXIT = Locations.ICONS.value + "exit.png"
        FOX = Locations.ICONS.value + "fox.png"
        LINE = Locations.ICONS.value + "line.png"
        NEW = Locations.ICONS.value + "new.png"
        OPEN = Locations.ICONS.value + "open.png"
        PALETTE = Locations.ICONS.value + "palette.png"
        ROUND = Locations.ICONS.value + "circle.png"
        SAVE = Locations.ICONS.value + "save.png"
        SQUARE = Locations.ICONS.value + "square.png"
        UNDO = Locations.ICONS.value + "undo.png"

        @staticmethod
        def hasKey(key):
            return key in Constants.Icons._member_names_
