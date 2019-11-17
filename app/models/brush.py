'''
    Brush
    A model representing our Brush

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen


class Brush:
    '''
        Brush has a set of attributes used to configure QPen
    '''
    # TODO : Move these to the constants class as enums
    capTypes = {
        'ROUND': Qt.RoundCap,
        'SQUARE': Qt.SquareCap,
        'FLAT': Qt.FlatCap
    }

    joinTypes = {
        'MITER': Qt.MiterJoin,
        'BEVEL': Qt.BevelJoin,
        'ROUND': Qt.RoundJoin
    }

    lineTypes = {
        'SOLID': Qt.SolidLine,
        'DASH': Qt.DashLine,
        'DOT': Qt.DotLine,
        'DASH_DOT': Qt.DashDotLine,
        'DASH_DOT_DOT': Qt.DashDotDotLine,
        'CUSTOM': Qt.CustomDashLine
    }

    def __init__(self):
        self.setDefaults()

    def getBrushType(self):
        '''
            Returns the type of brush

            Returns:
                (Constants.BrushTypes)
        '''
        return self.type

    def getColour(self):
        '''
            Returns the colour of the brush

            Returns:
                (QColor)
        '''
        return self.colour

    def getSize(self):
        '''
            Returns the current size of the brush in pixels

            Returns:
                (int)
        '''
        return self.size

    def getCapType(self):
        '''
            Returns the current cap on the brush
        '''
        return self.cap

    def getLineType(self):
        '''
            Returns the current line type in use
        '''
        return self.line

    def getJoinType(self):
        '''
            Returns the current join type
        '''
        return self.join

    def getAllLineTypes(self):
        '''
            Returns all the line types
        '''
        return self.lineTypes

    def getAllBrushTypes(self):
        '''
            Returns all of the brush types
        '''
        return dict(Constants.BrushTypes.__members__.items())

    def getAllCapTypes(self):
        '''
            Returns all of the cap types
        '''
        return self.capTypes

    def getAllJoinTypes(self):
        '''
            Returns all of the join types
        '''
        return self.joinTypes

    def setBrushType(self, type: str):
        '''
            Setter for brush type
        '''
        self.type = Constants.BrushTypes[type]

    def setColour(self, colour):
        '''
            Setter for colour
        '''
        self.colour = colour    # TODO: validation

    def setSize(self, size: int):
        '''
            Setter for size
        '''
        self.size = size

    def setLineType(self, type):
        '''
            Setter for line type
        '''
        line = self.lineTypes[type] if type in self.lineTypes else type
        if line not in self.lineTypes.values():
            raise ValueError('%s is not a valid line type' % (line))
        self.line = line

    def setCapType(self, type):
        '''
            Setter for cap type
        '''
        cap = self.capTypes[type] if type in self.capTypes else type
        if cap not in self.capTypes.values():
            raise ValueError('%s is not a valid cap type' % (cap))
        self.cap = cap

    def setJoinType(self, type):
        '''
            Setter for join type
        '''
        join = self.joinTypes[type] if type in self.joinTypes else type
        if join not in self.joinTypes.values():
            raise ValueError('%s is not a valid join type' % (join))
        self.join = join

    def setDefaults(self):
        '''
            Sets the defaults for the brush
        '''
        self.size = 10
        self.colour = Qt.red
        self.line = Qt.SolidLine
        self.cap = Qt.RoundCap
        self.join = Qt.RoundJoin
        self.type = Constants.BrushTypes.BRUSH

    def getPen(self):
        '''
            Returns a QPen using the current attributes

            Returns:
                (QPen)
        '''
        return QPen(self.colour, self.size, self.line, self.cap, self.join)

    def getPreviewPen(self):
        '''
            Returns a QPen with preview attributes

            Returns:
                (QPen)
        '''
        return QPen(Qt.black, 2, self.line, self.cap, self.join)
