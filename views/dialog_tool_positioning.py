# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/dialog_tool_positioning.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_positioning(object):
    def setupUi(self, Dialog_positioning):
        Dialog_positioning.setObjectName("Dialog_positioning")
        Dialog_positioning.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_positioning.resize(424, 227)
        Dialog_positioning.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_positioning)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog_positioning)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(6)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.widget_5 = QtWidgets.QWidget(self.groupBox_3)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setContentsMargins(-1, 0, 0, -1)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.spinBox_8 = QtWidgets.QSpinBox(self.widget_5)
        self.spinBox_8.setMinimum(-16700)
        self.spinBox_8.setMaximum(16700)
        self.spinBox_8.setSingleStep(10)
        self.spinBox_8.setObjectName("spinBox_8")
        self.verticalLayout_12.addWidget(self.spinBox_8)
        self.verticalSlider_2 = QtWidgets.QSlider(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider_2.sizePolicy().hasHeightForWidth())
        self.verticalSlider_2.setSizePolicy(sizePolicy)
        self.verticalSlider_2.setMinimum(-16700)
        self.verticalSlider_2.setMaximum(16700)
        self.verticalSlider_2.setSingleStep(10)
        self.verticalSlider_2.setProperty("value", 0)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.verticalLayout_12.addWidget(self.verticalSlider_2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_12)
        spacerItem = QtWidgets.QSpacerItem(92, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_11.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(self.groupBox_3)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider_2.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_2.setSizePolicy(sizePolicy)
        self.horizontalSlider_2.setMinimum(-16700)
        self.horizontalSlider_2.setMaximum(16700)
        self.horizontalSlider_2.setSingleStep(10)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalLayout_8.addWidget(self.horizontalSlider_2)
        self.spinBox_9 = QtWidgets.QSpinBox(self.widget_6)
        self.spinBox_9.setMinimum(-16700)
        self.spinBox_9.setMaximum(16700)
        self.spinBox_9.setSingleStep(10)
        self.spinBox_9.setObjectName("spinBox_9")
        self.horizontalLayout_8.addWidget(self.spinBox_9)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.verticalLayout_11.addWidget(self.widget_6)
        self.horizontalLayout.addWidget(self.groupBox_3)
        spacerItem2 = QtWidgets.QSpacerItem(0, 70, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.widget)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_positioning)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_positioning)
        self.buttonBox.accepted.connect(Dialog_positioning.accept)
        self.buttonBox.rejected.connect(Dialog_positioning.reject)
        self.verticalSlider_2.valueChanged['int'].connect(self.spinBox_8.setValue)
        self.spinBox_8.valueChanged['int'].connect(self.verticalSlider_2.setValue)
        self.horizontalSlider_2.valueChanged['int'].connect(self.spinBox_9.setValue)
        self.spinBox_9.valueChanged['int'].connect(self.horizontalSlider_2.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog_positioning)

    def retranslateUi(self, Dialog_positioning):
        _translate = QtCore.QCoreApplication.translate
        Dialog_positioning.setWindowTitle(_translate("Dialog_positioning", "Confocal image positioning"))
        self.groupBox_3.setTitle(_translate("Dialog_positioning", "Position offset [nm]"))

