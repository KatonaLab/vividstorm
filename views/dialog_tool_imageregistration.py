# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_imageregistration.ui'
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

class Ui_Dialog_imageregistration(object):
    def setupUi(self, Dialog_imageregistration):
        Dialog_imageregistration.setObjectName(_fromUtf8("Dialog_imageregistration"))
        Dialog_imageregistration.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_imageregistration.resize(658, 123)
        Dialog_imageregistration.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}"))
        self.formLayout = QtGui.QFormLayout(Dialog_imageregistration)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.widget = QtGui.QWidget(Dialog_imageregistration)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout_2 = QtGui.QFormLayout(self.widget)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.groupBox_3 = QtGui.QGroupBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_3.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.comboBox_storm_channel_changer = QtGui.QComboBox(self.groupBox_3)
        self.comboBox_storm_channel_changer.setObjectName(_fromUtf8("comboBox_storm_channel_changer"))
        self.gridLayout_3.addWidget(self.comboBox_storm_channel_changer, 1, 1, 1, 1)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_2 = QtGui.QGroupBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.comboBox_confocal_channel_changer = QtGui.QComboBox(self.groupBox_2)
        self.comboBox_confocal_channel_changer.setObjectName(_fromUtf8("comboBox_confocal_channel_changer"))
        self.gridLayout_4.addWidget(self.comboBox_confocal_channel_changer, 0, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_delete_markers = QtGui.QPushButton(self.widget)
        self.pushButton_delete_markers.setObjectName(_fromUtf8("pushButton_delete_markers"))
        self.horizontalLayout.addWidget(self.pushButton_delete_markers)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_manual_selection = QtGui.QPushButton(self.widget)
        self.pushButton_manual_selection.setObjectName(_fromUtf8("pushButton_manual_selection"))
        self.horizontalLayout.addWidget(self.pushButton_manual_selection)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton_automatic_selection = QtGui.QPushButton(self.widget)
        self.pushButton_automatic_selection.setObjectName(_fromUtf8("pushButton_automatic_selection"))
        self.horizontalLayout.addWidget(self.pushButton_automatic_selection)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_Registration = QtGui.QPushButton(self.widget)
        self.pushButton_Registration.setObjectName(_fromUtf8("pushButton_Registration"))
        self.horizontalLayout.addWidget(self.pushButton_Registration)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.LabelRole, self.gridLayout)
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.widget)

        self.retranslateUi(Dialog_imageregistration)
        QtCore.QMetaObject.connectSlotsByName(Dialog_imageregistration)

    def retranslateUi(self, Dialog_imageregistration):
        Dialog_imageregistration.setWindowTitle(_translate("Dialog_imageregistration", "Image registration tool", None))
        self.groupBox_3.setTitle(_translate("Dialog_imageregistration", "STORM channel", None))
        self.groupBox_2.setTitle(_translate("Dialog_imageregistration", "Confocal channel", None))
        self.pushButton_delete_markers.setText(_translate("Dialog_imageregistration", "Delete markers", None))
        self.pushButton_manual_selection.setText(_translate("Dialog_imageregistration", "Manual selection", None))
        self.pushButton_automatic_selection.setText(_translate("Dialog_imageregistration", "Automatic selection", None))
        self.pushButton_Registration.setText(_translate("Dialog_imageregistration", "Registration", None))

