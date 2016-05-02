# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_tool_positioning.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Dialog_positioning(object):
    def setupUi(self, Dialog_positioning):
        Dialog_positioning.setObjectName(_fromUtf8("Dialog_positioning"))
        Dialog_positioning.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_positioning.resize(424, 227)
        Dialog_positioning.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_positioning)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(Dialog_positioning)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_11.setMargin(0)
        self.verticalLayout_11.setSpacing(6)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.widget_5 = QtGui.QWidget(self.groupBox_3)
        self.widget_5.setObjectName(_fromUtf8("widget_5"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setMargin(0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.verticalLayout_12 = QtGui.QVBoxLayout()
        self.verticalLayout_12.setContentsMargins(-1, 0, 0, -1)
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.spinBox_8 = QtGui.QSpinBox(self.widget_5)
        self.spinBox_8.setMinimum(-16700)
        self.spinBox_8.setMaximum(16700)
        self.spinBox_8.setSingleStep(10)
        self.spinBox_8.setObjectName(_fromUtf8("spinBox_8"))
        self.verticalLayout_12.addWidget(self.spinBox_8)
        self.verticalSlider_2 = QtGui.QSlider(self.widget_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalSlider_2.sizePolicy().hasHeightForWidth())
        self.verticalSlider_2.setSizePolicy(sizePolicy)
        self.verticalSlider_2.setMinimum(-16700)
        self.verticalSlider_2.setMaximum(16700)
        self.verticalSlider_2.setSingleStep(10)
        self.verticalSlider_2.setProperty("value", 0)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName(_fromUtf8("verticalSlider_2"))
        self.verticalLayout_12.addWidget(self.verticalSlider_2)
        self.horizontalLayout_6.addLayout(self.verticalLayout_12)
        spacerItem = QtGui.QSpacerItem(92, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout_11.addWidget(self.widget_5)
        self.widget_6 = QtGui.QWidget(self.groupBox_3)
        self.widget_6.setObjectName(_fromUtf8("widget_6"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.widget_6)
        self.horizontalLayout_8.setMargin(0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.horizontalSlider_2 = QtGui.QSlider(self.widget_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider_2.sizePolicy().hasHeightForWidth())
        self.horizontalSlider_2.setSizePolicy(sizePolicy)
        self.horizontalSlider_2.setMinimum(-16700)
        self.horizontalSlider_2.setMaximum(16700)
        self.horizontalSlider_2.setSingleStep(10)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName(_fromUtf8("horizontalSlider_2"))
        self.horizontalLayout_8.addWidget(self.horizontalSlider_2)
        self.spinBox_9 = QtGui.QSpinBox(self.widget_6)
        self.spinBox_9.setMinimum(-16700)
        self.spinBox_9.setMaximum(16700)
        self.spinBox_9.setSingleStep(10)
        self.spinBox_9.setObjectName(_fromUtf8("spinBox_9"))
        self.horizontalLayout_8.addWidget(self.spinBox_9)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.verticalLayout_11.addWidget(self.widget_6)
        self.horizontalLayout.addWidget(self.groupBox_3)
        spacerItem2 = QtGui.QSpacerItem(0, 70, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.widget)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog_positioning)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog_positioning)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog_positioning.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog_positioning.reject)
        QtCore.QObject.connect(self.verticalSlider_2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spinBox_8.setValue)
        QtCore.QObject.connect(self.spinBox_8, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.verticalSlider_2.setValue)
        QtCore.QObject.connect(self.horizontalSlider_2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spinBox_9.setValue)
        QtCore.QObject.connect(self.spinBox_9, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.horizontalSlider_2.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog_positioning)

    def retranslateUi(self, Dialog_positioning):
        Dialog_positioning.setWindowTitle(_translate("Dialog_positioning", "Confocal image positioning", None))
        self.groupBox_3.setTitle(_translate("Dialog_positioning", "Position offset [nm]", None))

