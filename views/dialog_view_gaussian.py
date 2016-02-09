# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_view_gaussian.ui'
#
# Created: Tue Feb 09 14:49:11 2016
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

class Ui_Dialog_gaussian(object):
    def setupUi(self, Dialog_gaussian):
        Dialog_gaussian.setObjectName(_fromUtf8("Dialog_gaussian"))
        Dialog_gaussian.resize(346, 201)
        Dialog_gaussian.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_gaussian)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(Dialog_gaussian)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.formGroupBox = QtGui.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formGroupBox.setFont(font)
        self.formGroupBox.setObjectName(_fromUtf8("formGroupBox"))
        self.formLayout = QtGui.QFormLayout(self.formGroupBox)
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
        self.label = QtGui.QLabel(self.formGroupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.spinBox = QtGui.QSpinBox(self.formGroupBox)
        self.spinBox.setMinimum(5)
        self.spinBox.setMaximum(100)
        self.spinBox.setProperty("value", 10)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBox)
        self.label_3 = QtGui.QLabel(self.formGroupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.spinBox_3 = QtGui.QSpinBox(self.formGroupBox)
        self.spinBox_3.setMinimum(10)
        self.spinBox_3.setMaximum(100)
        self.spinBox_3.setProperty("value", 20)
        self.spinBox_3.setObjectName(_fromUtf8("spinBox_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBox_3)
        self.horizontalLayout_4.addWidget(self.formGroupBox)
        self.formGroupBox_2 = QtGui.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formGroupBox_2.setFont(font)
        self.formGroupBox_2.setObjectName(_fromUtf8("formGroupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.formGroupBox_2)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.radioButton = QtGui.QRadioButton(self.formGroupBox_2)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.formGroupBox_2)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.radioButton_2)
        self.horizontalLayout_4.addWidget(self.formGroupBox_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widget)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_gaussian)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_gaussian)
        QtCore.QMetaObject.connectSlotsByName(Dialog_gaussian)

    def retranslateUi(self, Dialog_gaussian):
        Dialog_gaussian.setWindowTitle(_translate("Dialog_gaussian", "Select STORM view mode - Gaussian", None))
        self.formGroupBox.setTitle(_translate("Dialog_gaussian", "Settings", None))
        self.label_2.setText(_translate("Dialog_gaussian", "Bin number", None))
        self.label.setText(_translate("Dialog_gaussian", "Min FWHM value [nm]", None))
        self.label_3.setText(_translate("Dialog_gaussian", "Resolution", None))
        self.formGroupBox_2.setTitle(_translate("Dialog_gaussian", "Display mode", None))
        self.radioButton.setText(_translate("Dialog_gaussian", "Addition", None))
        self.radioButton_2.setText(_translate("Dialog_gaussian", "Maximal intensity", None))

