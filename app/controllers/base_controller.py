'''
    Base Controller
    Base controller that will be extended from

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''
from PyQt5.QtWidgets import QWidget


class BaseController(QWidget):
    '''
        Base controller all classes will be derived from

        Args:
            signal (pyqtsignal): A pyqtsignal for this controller
    '''
    class Component:
        '''
            Wrapper for widgets, once added refer to them as components

            Args:
                widget (QWidget): The widget we want to control as a component
                callback (func) : A callback for the component
        '''
        def __init__(self, widget, callback=None):
            self.setWidget(widget, callback)

        def setWidget(self, widget, callback):
            '''
                Set the widget for this component, this allows us to swap this out
                dynamically in this component should we ever need to

                Args:
                    widget (QWidget): The widget we want to control as a component
                    callback (func) : A callback for the component
            '''
            self.widget = widget
            if callback is not None:
                if not widget.onChange:
                    raise ValueError(
                        "Widgets must have an onChange signal to be used as components"
                    )
                self.widget.onChange.connect(callback)

        def getWidget(self):
            '''
                Return the underlying widget

                Returns:
                    (QWidget)
            '''
            return self.widget

    def __init__(self, parent=None):
        super().__init__(parent)
        if self.update is None:
            raise RuntimeError("All controllers need an update signal")
        self.components = {}

    def makeComponent(self, widget, callback=None):
        '''
            Given a widget, and a callback, create a component and return this

            Args:
                widget (QWidget): The widget we want to control as a component
                callback (func) : A callback for the component

            Returns:
                (BaseController.Component)
        '''
        return BaseController.Component(widget, callback)

    def addComponents(self, components):
        '''
            Use a dict blueprint to add multiple components

            Args:
                components (dict): Dict keyed with name, and component
        '''
        for name, component in components.items():
            self.addComponent(name, component)

    def addComponent(self, name, component):
        '''
            Add a component by name to the controller

            Args:
                name (string):                        The unique name for the component
                component (BaseController.Component): The widget the controller will own
        '''
        if name in self.components:
            raise KeyError("%s already configured" % (name))
        if not isinstance(component, BaseController.Component):
            raise ValueError("Not a valid component, try using makeComponent")
        self.components[name] = component

    def getComponentWidget(self, name):
        '''
            Fetch a named component

            Returns:
                (QWidget)
        '''
        return self.components[name].getWidget(
        ) if name in self.components else None

    def getAllComponents(self):
        '''
            Fetch all the name components as a dict

            Returns:
                (Dict)
        '''
        return self.components
