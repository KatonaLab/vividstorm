# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/dialog_scale.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_scale(object):
    def setupUi(self, Dialog_scale):
        Dialog_scale.setObjectName("Dialog_scale")
        Dialog_scale.resize(260, 153)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_scale.sizePolicy().hasHeightForWidth())
        Dialog_scale.setSizePolicy(sizePolicy)
        Dialog_scale.setMaximumSize(QtCore.QSize(640, 480))
        Dialog_scale.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_scale)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_scale_5000 = QtWidgets.QPushButton(Dialog_scale)
        self.pushButton_scale_5000.setObjectName("pushButton_scale_5000")
        self.gridLayout.addWidget(self.pushButton_scale_5000, 1, 1, 1, 1)
        self.pushButton_scale_1000 = QtWidgets.QPushButton(Dialog_scale)
        self.pushButton_scale_1000.setObjectName("pushButton_scale_1000")
        self.gridLayout.addWidget(self.pushButton_scale_1000, 1, 0, 1, 1)
        self.pushButton_scale_100 = QtWidgets.QPushButton(Dialog_scale)
        self.pushButton_scale_100.setObjectName("pushButton_scale_100")
        self.gridLayout.addWidget(self.pushButton_scale_100, 0, 0, 1, 1)
        self.pushButton_scale_500 = QtWidgets.QPushButton(Dialog_scale)
        self.pushButton_scale_500.setObjectName("pushButton_scale_500")
        self.gridLayout.addWidget(self.pushButton_scale_500, 0, 1, 1, 1)
        self.pushButton_scale_10000 = QtWidgets.QPushButton(Dialog_scale)
        self.pushButton_scale_10000.setObjectName("pushButton_scale_10000")
        self.gridLayout.addWidget(self.pushButton_scale_10000, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButton_scale_0 = QtWidgets.QPushButton(Dialog_scale)
        self.pushButton_scale_0.setObjectName("pushButton_scale_0")
        self.verticalLayout.addWidget(self.pushButton_scale_0)

        self.retranslateUi(Dialog_scale)
        QtCore.QMetaObject.connectSlotsByName(Dialog_scale)

    def retranslateUi(self, Dialog_scale):
        _translate = QtCore.QCoreApplication.translate
        Dialog_scale.setWindowTitle(_translate("Dialog_scale", "Show scale"))
        self.pushButton_scale_5000.setText(_translate("Dialog_scale", "5 µm"))
        self.pushButton_scale_1000.setText(_translate("Dialog_scale", "1 µm"))
        self.pushButton_scale_100.setText(_translate("Dialog_scale", "100 nm"))
        self.pushButton_scale_500.setText(_translate("Dialog_scale", "500 nm"))
        self.pushButton_scale_10000.setText(_translate("Dialog_scale", "10 µm"))
        self.pushButton_scale_0.setText(_translate("Dialog_scale", "Hide scale"))

