# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_scale.ui'
#
# Created: Tue Feb 09 14:49:12 2016
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog_scale(object):
    def setupUi(self, Dialog_scale):
        Dialog_scale.setObjectName(_fromUtf8("Dialog_scale"))
        Dialog_scale.resize(260, 153)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_scale.sizePolicy().hasHeightForWidth())
        Dialog_scale.setSizePolicy(sizePolicy)
        Dialog_scale.setMaximumSize(QtCore.QSize(640, 480))
        Dialog_scale.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_scale)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_scale_5000 = QtGui.QPushButton(Dialog_scale)
        self.pushButton_scale_5000.setObjectName(_fromUtf8("pushButton_scale_5000"))
        self.gridLayout.addWidget(self.pushButton_scale_5000, 1, 1, 1, 1)
        self.pushButton_scale_1000 = QtGui.QPushButton(Dialog_scale)
        self.pushButton_scale_1000.setObjectName(_fromUtf8("pushButton_scale_1000"))
        self.gridLayout.addWidget(self.pushButton_scale_1000, 1, 0, 1, 1)
        self.pushButton_scale_100 = QtGui.QPushButton(Dialog_scale)
        self.pushButton_scale_100.setObjectName(_fromUtf8("pushButton_scale_100"))
        self.gridLayout.addWidget(self.pushButton_scale_100, 0, 0, 1, 1)
        self.pushButton_scale_500 = QtGui.QPushButton(Dialog_scale)
        self.pushButton_scale_500.setObjectName(_fromUtf8("pushButton_scale_500"))
        self.gridLayout.addWidget(self.pushButton_scale_500, 0, 1, 1, 1)
        self.pushButton_scale_10000 = QtGui.QPushButton(Dialog_scale)
        self.pushButton_scale_10000.setObjectName(_fromUtf8("pushButton_scale_10000"))
        self.gridLayout.addWidget(self.pushButton_scale_10000, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButton_scale_0 = QtGui.QPushButton(Dialog_scale)
        self.pushButton_scale_0.setObjectName(_fromUtf8("pushButton_scale_0"))
        self.verticalLayout.addWidget(self.pushButton_scale_0)

        self.retranslateUi(Dialog_scale)
        QtCore.QMetaObject.connectSlotsByName(Dialog_scale)

    def retranslateUi(self, Dialog_scale):
        Dialog_scale.setWindowTitle(_translate("Dialog_scale", "Show scale", None))
        self.pushButton_scale_5000.setText(_translate("Dialog_scale", "5 µm", None))
        self.pushButton_scale_1000.setText(_translate("Dialog_scale", "1 µm", None))
        self.pushButton_scale_100.setText(_translate("Dialog_scale", "100 nm", None))
        self.pushButton_scale_500.setText(_translate("Dialog_scale", "500 nm", None))
        self.pushButton_scale_10000.setText(_translate("Dialog_scale", "10 µm", None))
        self.pushButton_scale_0.setText(_translate("Dialog_scale", "Hide scale", None))

