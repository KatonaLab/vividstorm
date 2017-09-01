# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/dialog_tool_active_contour.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_active_contour(object):
    def setupUi(self, Dialog_active_contour):
        Dialog_active_contour.setObjectName("Dialog_active_contour")
        Dialog_active_contour.resize(341, 265)
        Dialog_active_contour.setStyleSheet("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_active_contour)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(58, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.radioButton_2D = QtWidgets.QRadioButton(Dialog_active_contour)
        self.radioButton_2D.setChecked(True)
        self.radioButton_2D.setObjectName("radioButton_2D")
        self.horizontalLayout_2.addWidget(self.radioButton_2D)
        spacerItem1 = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.radioButton_3D = QtWidgets.QRadioButton(Dialog_active_contour)
        self.radioButton_3D.setObjectName("radioButton_3D")
        self.horizontalLayout_2.addWidget(self.radioButton_3D)
        spacerItem2 = QtWidgets.QSpacerItem(78, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.formWidget = QtWidgets.QWidget(Dialog_active_contour)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formWidget.setFont(font)
        self.formWidget.setObjectName("formWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.formWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_confocal_channel_changer = QtWidgets.QComboBox(self.formWidget)
        self.comboBox_confocal_channel_changer.setObjectName("comboBox_confocal_channel_changer")
        self.gridLayout.addWidget(self.comboBox_confocal_channel_changer, 0, 1, 1, 1)
        self.spinBox_mu = QtWidgets.QSpinBox(self.formWidget)
        self.spinBox_mu.setMinimum(0)
        self.spinBox_mu.setMaximum(100)
        self.spinBox_mu.setProperty("value", 2)
        self.spinBox_mu.setObjectName("spinBox_mu")
        self.gridLayout.addWidget(self.spinBox_mu, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.formWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.spinBox_lambda2 = QtWidgets.QSpinBox(self.formWidget)
        self.spinBox_lambda2.setMinimum(0)
        self.spinBox_lambda2.setMaximum(100)
        self.spinBox_lambda2.setProperty("value", 2)
        self.spinBox_lambda2.setObjectName("spinBox_lambda2")
        self.gridLayout.addWidget(self.spinBox_lambda2, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.formWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.formWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.formWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.spinBox_lambda1 = QtWidgets.QSpinBox(self.formWidget)
        self.spinBox_lambda1.setMinimum(0)
        self.spinBox_lambda1.setMaximum(100)
        self.spinBox_lambda1.setProperty("value", 1)
        self.spinBox_lambda1.setObjectName("spinBox_lambda1")
        self.gridLayout.addWidget(self.spinBox_lambda1, 3, 1, 1, 1)
        self.spinBox_iteration_cycles = QtWidgets.QSpinBox(self.formWidget)
        self.spinBox_iteration_cycles.setMinimum(1)
        self.spinBox_iteration_cycles.setMaximum(500)
        self.spinBox_iteration_cycles.setProperty("value", 25)
        self.spinBox_iteration_cycles.setObjectName("spinBox_iteration_cycles")
        self.gridLayout.addWidget(self.spinBox_iteration_cycles, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.formWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.formWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.spinBox_dilation = QtWidgets.QSpinBox(self.formWidget)
        self.spinBox_dilation.setMinimum(0)
        self.spinBox_dilation.setMaximum(1000)
        self.spinBox_dilation.setProperty("value", 1)
        self.spinBox_dilation.setObjectName("spinBox_dilation")
        self.gridLayout.addWidget(self.spinBox_dilation, 5, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.formWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.checkBox_spline_fit = QtWidgets.QCheckBox(self.formWidget)
        self.checkBox_spline_fit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_spline_fit.setChecked(True)
        self.checkBox_spline_fit.setObjectName("checkBox_spline_fit")
        self.gridLayout.addWidget(self.checkBox_spline_fit, 6, 1, 1, 1)
        self.verticalLayout.addWidget(self.formWidget)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.pushButton_run = QtWidgets.QPushButton(Dialog_active_contour)
        self.pushButton_run.setObjectName("pushButton_run")
        self.horizontalLayout.addWidget(self.pushButton_run)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog_active_contour)
        QtCore.QMetaObject.connectSlotsByName(Dialog_active_contour)

    def retranslateUi(self, Dialog_active_contour):
        _translate = QtCore.QCoreApplication.translate
        Dialog_active_contour.setWindowTitle(_translate("Dialog_active_contour", "Active contour selector tool"))
        self.radioButton_2D.setText(_translate("Dialog_active_contour", "2D"))
        self.radioButton_3D.setText(_translate("Dialog_active_contour", "3D"))
        self.label_4.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels"))
        self.label_4.setText(_translate("Dialog_active_contour", "λ2 (Relative importance of outside pixels)"))
        self.label_2.setText(_translate("Dialog_active_contour", "Iteration cycles"))
        self.label.setText(_translate("Dialog_active_contour", "µ (smoothing parameter)"))
        self.label_3.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels"))
        self.label_3.setText(_translate("Dialog_active_contour", "λ1 (Relative importance of inside pixels)"))
        self.label_5.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels"))
        self.label_5.setText(_translate("Dialog_active_contour", "Confocal channel"))
        self.label_6.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels"))
        self.label_6.setText(_translate("Dialog_active_contour", "Dilation (pixel)"))
        self.label_7.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels"))
        self.label_7.setText(_translate("Dialog_active_contour", "Spline fit"))
        self.pushButton_run.setText(_translate("Dialog_active_contour", "Start contour evolution"))

