# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_view_3d.ui'
#
# Created: Sat Oct 10 18:11:34 2015
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

class Ui_Dialog_3d(object):
    def setupUi(self, Dialog_3d):
        Dialog_3d.setObjectName(_fromUtf8("Dialog_3d"))
        Dialog_3d.resize(331, 163)
        Dialog_3d.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_3d)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(Dialog_3d)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.formGroupBox = QtGui.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formGroupBox.setFont(font)
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.formLayout = QtGui.QFormLayout(self.formGroupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(9)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(self.formGroupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.spinBox_2 = QtGui.QSpinBox(self.formGroupBox)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(100)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBox_2)
        self.horizontalLayout.addWidget(self.formGroupBox)
        self.formGroupBox_2 = QtGui.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formGroupBox_2.setFont(font)
        self.formGroupBox_2.setCheckable(True)
        self.formGroupBox_2.setObjectName(_fromUtf8("formGroupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.formGroupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_3 = QtGui.QLabel(self.formGroupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.spinBox_3 = QtGui.QSpinBox(self.formGroupBox_2)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(100)
        self.spinBox_3.setProperty("value", 70)
        self.spinBox_3.setObjectName(_fromUtf8("spinBox_3"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBox_3)
        self.horizontalLayout.addWidget(self.formGroupBox_2)
        spacerItem = QtGui.QSpacerItem(0, 70, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widget)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_3d)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_3d)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_3d.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_3d.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_3d)

    def retranslateUi(self, Dialog_3d):
        Dialog_3d.setWindowTitle(_translate("Dialog_3d", "Select STORM view mode - 3D", None))
        self.formGroupBox.setTitle(_translate("Dialog_3d", "Settings", None))
        self.label_2.setText(_translate("Dialog_3d", "Size", None))
        self.formGroupBox_2.setTitle(_translate("Dialog_3d", "Show convex hull", None))
        self.label_3.setText(_translate("Dialog_3d", "Transparency", None))

