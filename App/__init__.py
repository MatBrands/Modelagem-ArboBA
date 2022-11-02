from PyQt5 import QtWidgets
from Model.Gui import *
    
if __name__ == '__main__':
    
    app = QtWidgets.QApplication([])
  
    start = AppGui()
    
    app.exec()