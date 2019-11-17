'''
    Layouts for our views
    Each of the layouts extend from the base layouts

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from app.lib.constants import Constants
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFormLayout, QGroupBox, QBoxLayout, QHBoxLayout,
                             QLayout, QVBoxLayout, QWidget)


class BaseGroupedLayout(QBoxLayout):
    '''
        Base grouped layout for widgets as we tend to use groupings

        Args:
            direction (QBoxLayout.DIRECTION): The direction for the layout
    '''
    def __init__(self, direction, parent=None):
        super().__init__(direction, parent)
        self.groups = []
        self.groupIndex = 0
        self.currentGroupIndex = 0
        self.currentGroup = None

    def addToCurrentGroup(self, *components):
        '''
            Used to add components to the current group

            Args:
                components (iterable): Widgets/layouts to add to the group
        '''

        for component in components:
            # add widget is only available on a layout that we have added to the QGroupBox
            if isinstance(component, QWidget):
                self.groups[self.groupIndex].addWidget(component)
            elif isinstance(component, QLayout):
                self.groups[self.groupIndex].addLayout(component)

    def addToExistingGroup(self, index: int, component):
        '''
            Add a component to a different group

            Args:
                index (int):                    The existing group index
                component (QWidget/QLayout):    The component to aadd
        '''
        if index not in self.groups:
            raise IndexError("Group at index is not set")
        if isinstance(component, QWidget):
            self.groups[index].addWidget(component)
        elif isinstance(component, QLayout):
            self.groups[index].addLayout(component)

    def createGroup(self, layout, label=None, sizePolicy=None):
        '''
            Create a new group with a specific layout

            Args:
                layout (QBoxLayout):    A layout to use
                label (str):            A label for the group
                sizePolicy (tuple):     QSizePolicy for horizontal and vertical
        '''
        self.currentGroup = QGroupBox(label)
        if sizePolicy:
            self.currentGroup.setSizePolicy(*sizePolicy)
        self.groups.append(layout)

    def flattenCurrentGroup(self):
        self.currentGroup.setFlat(True)

    def finishGroup(self):
        '''
            A finish method to build the layout
        '''
        self.currentGroup.setLayout(self.groups[self.groupIndex])
        self.addWidget(self.currentGroup)
        self.currentGroup = None
        self.groupIndex += 1

    def createVerticalGroup(self, label=None, sizePolicy=None, align=None):
        '''
            Create a new group with a vertical layout

            Args:
                label (str):         A label for the group
                sizePolicy (tuple):  QSizePolicy for horizontal and vertical
                align (QtAlign):     Align the contents
        '''
        layout = self.getVerticalLayout()
        if align:
            layout.setAlignment(align)
        self.createGroup(self.getVerticalLayout(), label, sizePolicy)

    def createHorizontalGroup(self, label=None, sizePolicy=None, align=None):
        '''
            Create a new group with a horizontal layout

            Args:
                label (str):         A label for the group
                sizePolicy (tuple):  QSizePolicy for horizontal and vertical
                align (QtAlign):     Align the contents
        '''
        layout = self.getHorizontalLayout()
        if align:
            layout.setAlignment(align)
        self.createGroup(self.getHorizontalLayout(), label, sizePolicy)

    def getFormLayout(self):
        '''
            Helper to create a new form layout

            Returns:
                (QFormLayout)
        '''
        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        return layout

    def getHorizontalLayout(self):
        '''
            Helper to create a new horizontal layout

            Returns:
                (QHBoxLayout)
        '''
        return QHBoxLayout()

    def getVerticalLayout(self):
        '''
            Helper to create a new vertical layout

            Returns:
                (QVBoxLayout)
        '''
        return QVBoxLayout()

    def setLayoutOfCurrentGroup(self, layout):
        '''
            Helper to set the layout of the current group

            Args:
                layout (QBoxLayout): The Layout to set
        '''
        self.groups[self.groupIndex].addLayout(layout)


class BaseRowGroupedLayout(BaseGroupedLayout):
    '''
        Wrapper for BaseGroupedLayout
    '''
    def __init__(self, parent=None):
        super().__init__(QBoxLayout.TopToBottom, parent)


class BaseColumnGroupedLayout(BaseGroupedLayout):
    '''
        Wrapper for BaseGroupedLayout
    '''
    def __init__(self, parent=None):
        super().__init__(QBoxLayout.LeftToRight, parent)


class MainLayout(QVBoxLayout):
    '''
        Main layout for the window

        Args:
            components (QWidget): Widgets
    '''
    def __init__(self, canvas, brushSettings):
        super().__init__()
        canvas.setSizePolicy(*Constants.AUTO_WIDTH_AUTO_HEIGHT)
        self.addWidget(canvas)
        brushSettings.setSizePolicy(*Constants.AUTO_WIDTH_FIXED_HEIGHT)
        self.addWidget(brushSettings)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(20)


class BrushSettingsLayout(BaseColumnGroupedLayout):
    '''
        Layout for the brush controls

        Args:
            components (QWidgets): Widgets
    '''
    def __init__(self, *components):
        super().__init__()
        # Create a vertical grouping that expands horizontally
        # and is fixed vertically
        self.createVerticalGroup(None, Constants.AUTO_WIDTH_FIXED_HEIGHT,
                                 Qt.AlignTop)
        self.flattenCurrentGroup()
        # Create a column based group layour
        settings = BaseColumnGroupedLayout()
        for i, component in enumerate(components):

            key, value = next(iter(component.items()))
            settings.createVerticalGroup(key)
            layout = self.getFormLayout()

            for label, widget in value.items():
                if label is not None:
                    layout.addRow(label, widget)
                else:
                    for sub in (widget
                                if isinstance(widget, list) else list(widget)):
                        layout.addRow(sub)

            settings.addToCurrentGroup(layout)
            settings.finishGroup()
        self.addToCurrentGroup(settings)
        self.finishGroup()


class BrushSizeLayout(QVBoxLayout):
    '''
        Layout for the brush size

        Args:
            label   (str):      label for the slider
            slider  (QWidget):  Widget for altering the size
    '''
    def __init__(self, label, slider):
        super().__init__()
        self.addWidget(slider)
        label.setMinimumWidth(40)
        self.addWidget(label)
