# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui\dialog_tool_active_contour.ui'
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

class Ui_Dialog_active_contour(object):
    def setupUi(self, Dialog_active_contour):
        Dialog_active_contour.setObjectName(_fromUtf8("Dialog_active_contour"))
        Dialog_active_contour.resize(341, 265)
        Dialog_active_contour.setStyleSheet(_fromUtf8("QWidget{\n"
"    background-color: rgb(67, 67, 67);\n"
"    color: rgb(255, 255, 255);\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_active_contour)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(58, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.radioButton_2D = QtGui.QRadioButton(Dialog_active_contour)
        self.radioButton_2D.setChecked(True)
        self.radioButton_2D.setObjectName(_fromUtf8("radioButton_2D"))
        self.horizontalLayout_2.addWidget(self.radioButton_2D)
        spacerItem1 = QtGui.QSpacerItem(68, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.radioButton_3D = QtGui.QRadioButton(Dialog_active_contour)
        self.radioButton_3D.setObjectName(_fromUtf8("radioButton_3D"))
        self.horizontalLayout_2.addWidget(self.radioButton_3D)
        spacerItem2 = QtGui.QSpacerItem(78, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtGui.QSpacerItem(20, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.formWidget = QtGui.QWidget(Dialog_active_contour)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.formWidget.setFont(font)
        self.formWidget.setObjectName(_fromUtf8("formWidget"))
        self.gridLayout = QtGui.QGridLayout(self.formWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboBox_confocal_channel_changer = QtGui.QComboBox(self.formWidget)
        self.comboBox_confocal_channel_changer.setObjectName(_fromUtf8("comboBox_confocal_channel_changer"))
        self.gridLayout.addWidget(self.comboBox_confocal_channel_changer, 0, 1, 1, 1)
        self.spinBox_mu = QtGui.QSpinBox(self.formWidget)
        self.spinBox_mu.setMinimum(0)
        self.spinBox_mu.setMaximum(100)
        self.spinBox_mu.setProperty("value", 2)
        self.spinBox_mu.setObjectName(_fromUtf8("spinBox_mu"))
        self.gridLayout.addWidget(self.spinBox_mu, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.formWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.spinBox_lambda2 = QtGui.QSpinBox(self.formWidget)
        self.spinBox_lambda2.setMinimum(0)
        self.spinBox_lambda2.setMaximum(100)
        self.spinBox_lambda2.setProperty("value", 2)
        self.spinBox_lambda2.setObjectName(_fromUtf8("spinBox_lambda2"))
        self.gridLayout.addWidget(self.spinBox_lambda2, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.formWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.formWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.formWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.spinBox_lambda1 = QtGui.QSpinBox(self.formWidget)
        self.spinBox_lambda1.setMinimum(0)
        self.spinBox_lambda1.setMaximum(100)
        self.spinBox_lambda1.setProperty("value", 1)
        self.spinBox_lambda1.setObjectName(_fromUtf8("spinBox_lambda1"))
        self.gridLayout.addWidget(self.spinBox_lambda1, 3, 1, 1, 1)
        self.spinBox_iteration_cycles = QtGui.QSpinBox(self.formWidget)
        self.spinBox_iteration_cycles.setMinimum(1)
        self.spinBox_iteration_cycles.setMaximum(500)
        self.spinBox_iteration_cycles.setProperty("value", 25)
        self.spinBox_iteration_cycles.setObjectName(_fromUtf8("spinBox_iteration_cycles"))
        self.gridLayout.addWidget(self.spinBox_iteration_cycles, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.formWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.formWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.spinBox_dilation = QtGui.QSpinBox(self.formWidget)
        self.spinBox_dilation.setMinimum(0)
        self.spinBox_dilation.setMaximum(1000)
        self.spinBox_dilation.setProperty("value", 1)
        self.spinBox_dilation.setObjectName(_fromUtf8("spinBox_dilation"))
        self.gridLayout.addWidget(self.spinBox_dilation, 5, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.formWidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.checkBox_spline_fit = QtGui.QCheckBox(self.formWidget)
        self.checkBox_spline_fit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_spline_fit.setChecked(True)
        self.checkBox_spline_fit.setObjectName(_fromUtf8("checkBox_spline_fit"))
        self.gridLayout.addWidget(self.checkBox_spline_fit, 6, 1, 1, 1)
        self.verticalLayout.addWidget(self.formWidget)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.pushButton_run = QtGui.QPushButton(Dialog_active_contour)
        self.pushButton_run.setObjectName(_fromUtf8("pushButton_run"))
        self.horizontalLayout.addWidget(self.pushButton_run)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog_active_contour)
        QtCore.QMetaObject.connectSlotsByName(Dialog_active_contour)

    def retranslateUi(self, Dialog_active_contour):
        Dialog_active_contour.setWindowTitle(_translate("Dialog_active_contour", "Active contour selector tool", None))
        self.radioButton_2D.setText(_translate("Dialog_active_contour", "2D", None))
        self.radioButton_3D.setText(_translate("Dialog_active_contour", "3D", None))
        self.label_4.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels", None))
        self.label_4.setText(_translate("Dialog_active_contour", "λ2 (Relative importance of outside pixels)", None))
        self.label_2.setText(_translate("Dialog_active_contour", "Iteration cycles", None))
        self.label.setText(_translate("Dialog_active_contour", "µ (smoothing parameter)", None))
        self.label_3.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels", None))
        self.label_3.setText(_translate("Dialog_active_contour", "λ1 (Relative importance of inside pixels)", None))
        self.label_5.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels", None))
        self.label_5.setText(_translate("Dialog_active_contour", "Confocal channel", None))
        self.label_6.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels", None))
        self.label_6.setText(_translate("Dialog_active_contour", "Dilation (pixel)", None))
        self.label_7.setToolTip(_translate("Dialog_active_contour", "Relative importance of the inside pixels", None))
        self.label_7.setText(_translate("Dialog_active_contour", "Spline fit", None))
        self.pushButton_run.setText(_translate("Dialog_active_contour", "Start contour evolution", None))

