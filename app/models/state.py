'''
    A base state object

    Author:
        Matthew Barber <mfmbarber@gmail.com>
'''


class State:
    def printState(self):
        '''
            A method that is overriden by child classes

            Returns:
                (str)
        '''
        return ""

    def __str__(self):
        '''
            Magic method to print a string

            Returns:
                (str)
        '''
        return self.printState()
