'''
    Painter Entry Point
    Author: Matthew Barber<mfmbarber@gmail.com>
'''

import sys

from app.painter import Painter
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Painter()
    sys.exit(app.exec_())
