# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_help.ui'
#
# Created: Sat Oct 10 18:11:32 2015
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

class Ui_Dialog_help_2(object):
    def setupUi(self, Dialog_help_2):
        Dialog_help_2.setObjectName(_fromUtf8("Dialog_help_2"))
        Dialog_help_2.resize(274, 258)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_help_2.sizePolicy().hasHeightForWidth())
        Dialog_help_2.setSizePolicy(sizePolicy)
        Dialog_help_2.setMaximumSize(QtCore.QSize(640, 480))
        Dialog_help_2.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_help_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.Dialog_help = QtGui.QPlainTextEdit(Dialog_help_2)
        self.Dialog_help.setObjectName(_fromUtf8("Dialog_help"))
        self.verticalLayout.addWidget(self.Dialog_help)
        self.label = QtGui.QLabel(Dialog_help_2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_help_2)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_help_2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_help_2.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_help_2.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_help_2)

    def retranslateUi(self, Dialog_help_2):
        Dialog_help_2.setWindowTitle(_translate("Dialog_help_2", "VividSTORM help", None))
        self.Dialog_help.setPlainText(_translate("Dialog_help_2", "VividSTORM User Guide can be downloaded from:\n"
"www.katonalab/VividSTORM\n"
"\n"
"", None))

