import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1158, 818)
        self.background = QtWidgets.QLabel(Dialog)
        self.background.setGeometry(QtCore.QRect(4, -5, 1161, 821))
        self.background.setGeometry(QtCore.QRect(4, -5, 1161, 821))
        self.background.setPixmap(QtGui.QPixmap(resource_path("background.jpg")))
        self.background.setObjectName("background")
        self.circle = QtWidgets.QLabel(Dialog)
        self.circle.setGeometry(QtCore.QRect(60, 100, 301, 281))
        self.revolve = QMovie(resource_path("circle.gif"))
        self.circle.setMovie(self.revolve)
        self.revolve.start()
        self.circle.setObjectName("circle")
        self.wave = QtWidgets.QLabel(Dialog)
        self.wave.setGeometry(QtCore.QRect(10, 450, 521, 261))
        self.waves = QMovie(resource_path("waves.gif"))
        self.wave.setMovie(self.waves)
        self.waves.start()
        self.wave.setScaledContents(True)
        self.wave.setObjectName("wave")
        self.textBox = QtWidgets.QTextEdit(Dialog)
        self.textBox.setGeometry(QtCore.QRect(20, 691, 471, 71))
        self.textBox.setStyleSheet("background-color :rgb(56, 56, 56);\n"
"color : rgb(255, 255, 255);\n"
"font: 14pt \"Times New Roman\";")
        self.textBox.setObjectName("textBox")
        self.btn_i = QtWidgets.QPushButton(Dialog)
        self.btn_i.setGeometry(QtCore.QRect(780, 300, 93, 28))
        self.btn_i.setObjectName("btn_i")
        self.btn_j = QtWidgets.QPushButton(Dialog)
        self.btn_j.setGeometry(QtCore.QRect(780, 360, 93, 28))
        self.btn_j.setText("")
        self.btn_j.setObjectName("btn_j")
        self.btn_j.raise_()
        self.btn_i.raise_()
        self.background.raise_()
        self.circle.raise_()
        self.wave.raise_()
        self.textBox.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_i.setText(_translate("Dialog", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())