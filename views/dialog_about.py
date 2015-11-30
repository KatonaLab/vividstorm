# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_about.ui'
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

class Ui_Dialog_about(object):
    def setupUi(self, Dialog_about):
        Dialog_about.setObjectName(_fromUtf8("Dialog_about"))
        Dialog_about.resize(466, 266)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_about.sizePolicy().hasHeightForWidth())
        Dialog_about.setSizePolicy(sizePolicy)
        Dialog_about.setMaximumSize(QtCore.QSize(640, 480))
        Dialog_about.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_about)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Dialog_about)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.label = QtGui.QLabel(Dialog_about)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_about)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_about)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_about.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_about.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_about)

    def retranslateUi(self, Dialog_about):
        Dialog_about.setWindowTitle(_translate("Dialog_about", "About VividSTORM", None))
        self.plainTextEdit.setPlainText(_translate("Dialog_about", "VividSTORM version 1.3.1\n"
"\n"
"Copyright © 2015 László Barna, Barna Dudok, Vivien Miczán, András Horváth and István Katona\n"
"This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.\n"
"\n"
"This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details: https://www.gnu.org/licenses/gpl-3.0.html\n"
"", None))

