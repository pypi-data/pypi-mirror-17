#example9 QtRPT, Aleksey Osipov, E-mail: aliks-os@ukr.net
# to pyside Numael Garay, numaelis@gmail.com

#Report with Drawing

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import QtCore
from PyQtRPT import PyQtRPT


a = QApplication(sys.argv)
form = QDialog()
report= PyQtRPT.QtRPT()

report.loadReport("examples_report/example9.xml")
#bac=QPixmap("examples/examples_report/qt_background_portrait.png")
#report.setBackgroundImage(bac)


report.printExec()
form.show()
a.exec_()
