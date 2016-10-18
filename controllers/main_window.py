# -*- coding: utf-8 -*-
"""
Created on: 2014.12.30.

Author: turbo


"""

from PyQt4 import QtCore, QtGui
# from views.main_window import Ui_MainWindow
import default_config
from views.main_window import Ui_MainWindow
from viewer.viewer import Viewer
from dialogs import *
from images import *
from rois import FreehandRoi
from settings import *
import os
import analyses as anal
import autoregistration

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


class MainWindow(Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()

        self.viewer = None
        self.storm_settings = StormSettings()
        self.confocal_settings = ConfocalSettings()
        if not os.path.isfile('WorkDir.ini'):
            file('WorkDir.ini', 'w').close()
        f = open('WorkDir.ini', 'r')
        
        workdirCandidate=f.read()
        if os.path.isdir(workdirCandidate):
            self.working_directory=workdirCandidate
        else:
            self.working_directory=os.getcwd()
        self.working_directory_unset = True
        f.close()      
        try:
            os.makedirs(self.working_directory)
        except OSError:
            if not os.path.isdir(self.working_directory):
                raise

    def init_component(self, qt_window):
        self.qt_window = qt_window
        self._create_dialogs()
        self._setup_components()
        self._add_handlers()
        self.status_bar = QtGui.QStatusBar()
        self.qt_window.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Welcome to VividSTORM")

    def _setup_components(self):
        self.viewer = Viewer(main_window=self)
        self.viewer.change_drag_mode(self.actionDragging_mode.isChecked())
        self.storm_settings.setup(self, 'storm')
        self.storm_settings.set_default_values()
        self.storm_settings.setup_filters()

        self.confocal_settings.setup(self, 'confocal')
        self.confocal_settings.set_default_values()

        self.dialog_tool_analysis.setup()
        self.dialog_tool_lut.setup()
        self.dialog_tool_active_contour.setup()
        self.dialog_imageregistration.setup()

    def _add_dialog(self, new_dialog):
        qtDialog = QtGui.QDialog()
        new_dialog.setupUi(qtDialog)
        new_dialog.qtDialog = qtDialog
        new_dialog.main_window = self
        return new_dialog

    def _create_dialogs(self):
        self.dialog_tool_lut = self._add_dialog(LutDialog())
        self.dialog_tool_active_contour = self._add_dialog(ActiveContourDialog())
        
        self.dialog_tool_analysis = self._add_dialog(AnalysisDialog())
        self.dialog_view_dots = self._add_dialog(DotsDialog())
        self.dialog_view_gaussian = self._add_dialog(GaussianDialog())
        self.dialog_view_3d = self._add_dialog(ThreeDDialog())
        self.dialog_scale = self._add_dialog(ScaleDialog())
        self.dialog_loading = self._add_dialog(LoadingDialog())
        self.dialog_error = self._add_dialog(ErrorDialog())
        self.dialog_about=self._add_dialog(AboutDialog())
        self.dialog_help=self._add_dialog(HelpDialog())
        self.dialog_imageregistration = self._add_dialog(ImageRegistrationDialog())
        

    def _add_action_handlers(self):
        self.actionOpen_STORM_files.triggered.connect(lambda: self._open_files('storm'))
        self.actionClose_STORM_files.triggered.connect(lambda: self._close_files('storm'))
        self.actionOpen_Confocal_files.triggered.connect(lambda: self._open_files('confocal'))
        self.actionClose_Confocal_files.triggered.connect(lambda: self._close_files('confocal'))

        self.actionSet_working_directory.triggered.connect(self._set_working_directory)
        # self.actionExport_As_Image.triggered.connect(lambda: self._export_as_image())

        self.actionDots.triggered.connect(lambda: self._open_dialog(self.dialog_view_dots))
        self.actionGaussian.triggered.connect(lambda: self._open_dialog(self.dialog_view_gaussian))
        self.action3D.triggered.connect(lambda: self._open_dialog(self.dialog_view_3d))

        self.actionFreehand_selecting.triggered.connect(lambda: self._draw_roi('freehand'))
        self.actionEllipse_ROI_selecting.triggered.connect(lambda: self._draw_roi('ellipse'))
        self.actionCircle_ROI_selecting.triggered.connect(lambda: self._draw_roi('circle'))
        self.actionActiveContour_selector.triggered.connect(lambda: self._open_dialog(self.dialog_tool_active_contour))
        self.actionDelete_ROI_selector.triggered.connect(lambda: self.viewer.remove_roi(self.storm_roi_list.currentItem()))
        self.actionJoin_Result_files_in_a_folder.triggered.connect(lambda: anal.JoinResults( self.working_directory))
        self.actionJoin_ROI_attribute_files_in_a_folder.triggered.connect(lambda: anal.JoinROIs(self, self.working_directory))

        self.actionShow_1_m_scale.triggered.connect(lambda: self._open_dialog(self.dialog_scale))
        self.actionDragging_mode.triggered.connect(lambda: self.viewer.change_drag_mode(self.actionDragging_mode.isChecked()))
        self.actionLUT_changer.triggered.connect(lambda: self._open_dialog(self.dialog_tool_lut))
        self.actionAnalysis.triggered.connect(lambda: self._open_dialog(self.dialog_tool_analysis))

        self.actionAbout_VividSTORM.triggered.connect(lambda: self._open_dialog(self.dialog_about))
        self.actionVividSTORM_help.triggered.connect(lambda: self._open_dialog(self.dialog_help))
        self.actionImage_Registration.triggered.connect(lambda: self._open_dialog(self.dialog_imageregistration))

        self.actionImage_AutomaticRegistration.triggered.connect(lambda: self._automatic_registration())


    def _add_key_shortcuts(self):
        QtCore.QObject.connect(
            QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageDown), self.pushButton_next_batch),
            QtCore.SIGNAL('activated()'),
            lambda: self._batch_step_files_by(1))
        QtCore.QObject.connect(
            QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageUp), self.pushButton_prev_batch),
            QtCore.SIGNAL('activated()'),
            lambda: self._batch_step_files_by(-1))

    def _add_input_handlers(self):
        self.pushButton_open_storm.clicked.connect(lambda: self._open_files('storm'))
        self.pushButton_open_confocal.clicked.connect(lambda: self._open_files('confocal'))
        self.pushButton_unload_storm.clicked.connect(
            lambda: self.viewer.unload_storm_image(self.storm_images_list.currentItem()))
        self.pushButton_unload_confocal.clicked.connect(
            lambda: self.viewer.unload_confocal_image(self.confocal_images_list.currentItem()))
        self.pushButton_close_all_storm.clicked.connect(lambda: self._close_files('storm'))
        self.pushButton_close_all_confocal.clicked.connect(lambda: self._close_files('confocal'))
        self.pushButton_close_storm.clicked.connect(
            lambda: self._close_file('storm', self.storm_images_list.currentRow()))
        self.pushButton_close_confocal.clicked.connect(
            lambda: self._close_file('confocal', self.confocal_images_list.currentRow()))
        self.pushButton_next_batch.clicked.connect(lambda: self._batch_step_files_by(1))
        self.pushButton_prev_batch.clicked.connect(lambda: self._batch_step_files_by(-1))
        self.pushButton_show_storm.clicked.connect(
            lambda: self.viewer.show_storm_image(self.storm_images_list.currentItem()))
        self.pushButton_show_confocal.clicked.connect(
            lambda: self.viewer.show_confocal_image(self.confocal_images_list.currentItem()))

        self.pushButton_unselect_roi.clicked.connect(
            lambda: self.storm_roi_list.setCurrentRow(-1))
        self.pushButton_delete_roi.clicked.connect(
            lambda: self.viewer.remove_roi(self.storm_roi_list.currentItem()))


        self.checkBox_storm_channel0.stateChanged.connect(
            lambda: self.viewer.display.SetStormChannelVisible(0, self.checkBox_storm_channel0.isChecked()))
        self.checkBox_storm_channel1.stateChanged.connect(
            lambda: self.viewer.display.SetStormChannelVisible(1, self.checkBox_storm_channel1.isChecked()))
        self.checkBox_storm_channel2.stateChanged.connect(
            lambda: self.viewer.display.SetStormChannelVisible(2, self.checkBox_storm_channel2.isChecked()))
        self.checkBox_storm_channel3.stateChanged.connect(
            lambda: self.viewer.display.SetStormChannelVisible(3, self.checkBox_storm_channel3.isChecked()))

        self.comboBox_storm_channel0_color.currentIndexChanged.connect(
            lambda: self.viewer.display.SetStormChannelColor(
                0, str(self.comboBox_storm_channel0_color.currentText())))
        self.comboBox_storm_channel1_color.currentIndexChanged.connect(
            lambda: self.viewer.display.SetStormChannelColor(
                1, str(self.comboBox_storm_channel1_color.currentText())))
        self.comboBox_storm_channel2_color.currentIndexChanged.connect(
            lambda: self.viewer.display.SetStormChannelColor(
                2, str(self.comboBox_storm_channel2_color.currentText())))
        self.comboBox_storm_channel3_color.currentIndexChanged.connect(
            lambda: self.viewer.display.SetStormChannelColor(
                3, str(self.comboBox_storm_channel3_color.currentText())))

        self.checkBox_confocal_channel0.stateChanged.connect(
            lambda: self.viewer.display.SetConfocalChannelVisible(0, self.checkBox_confocal_channel0.isChecked()))
        self.checkBox_confocal_channel1.stateChanged.connect(
            lambda: self.viewer.display.SetConfocalChannelVisible(1, self.checkBox_confocal_channel1.isChecked()))
        self.checkBox_confocal_channel2.stateChanged.connect(
            lambda: self.viewer.display.SetConfocalChannelVisible(2, self.checkBox_confocal_channel2.isChecked()))
        self.checkBox_confocal_channel3.stateChanged.connect(
            lambda: self.viewer.display.SetConfocalChannelVisible(3, self.checkBox_confocal_channel3.isChecked()))

        self.comboBox_confocal_channel0_color.currentIndexChanged.connect(
            lambda: self.viewer.display.SetConfocalChannelColor(
                0, str(self.comboBox_confocal_channel0_color.currentText())))
        self.comboBox_confocal_channel1_color.currentIndexChanged.connect(
            lambda: self.viewer.display.SetConfocalChannelColor(
                1, str(self.comboBox_confocal_channel1_color.currentText())))
        self.comboBox_confocal_channel2_color.currentIndexChanged.connect(
            lambda: self.viewer.display.SetConfocalChannelColor(
                2, str(self.comboBox_confocal_channel2_color.currentText())))
        self.comboBox_confocal_channel3_color.currentIndexChanged.connect(
            lambda: self.viewer.display.SetConfocalChannelColor(
                3, str(self.comboBox_confocal_channel3_color.currentText())))


    def _add_event_handlers(self):
        self.storm_images_list.currentItemChanged.connect(self.storm_settings.apply_storm_config)
        self.confocal_images_list.currentItemChanged.connect(self.viewer.show_confocal_image)


    def _add_handlers(self):
        self._add_action_handlers()
        self._add_key_shortcuts()
        self._add_input_handlers()
        self._add_event_handlers()

    def show_loading(self, title=u'Please wait', message=u'Loading...'):
        self.dialog_loading.setWindowTitle(title)
        self.dialog_loading.findChild(QtGui.QLabel, 'label').setText(message)
        self._open_dialog(self.dialog_loading)

    def finish_loading(self):
        self.dialog_loading.close()

    def show_error(self, title=u'Attention', message=u'Something happened'):
        self.dialog_error.qtDialog.setWindowTitle(title)
        self.dialog_error.qtDialog.findChild(QtGui.QLabel, 'label').setText(message)
        self._open_dialog(self.dialog_error)

    def _set_working_directory(self):
        #try to read the file        
        if not os.path.isfile('WorkDir.ini'):
            file('WorkDir.ini', 'w').close()
        f = open('WorkDir.ini', 'r')
        workdirCandidate=f.read()
        if os.path.isdir(workdirCandidate):
            self.working_directory=workdirCandidate
        else:
            self.working_directory=os.getcwd()
        self.working_directory_unset = True
        f.close()
        file_dialog = QtGui.QFileDialog()
        working_directory = QtGui.QFileDialog.getExistingDirectory(file_dialog, 'Select working directory',
                                                                   self.working_directory)
        if working_directory.length() > 0:
            self.working_directory = str(working_directory)
            self.working_directory_unset = False
        #write working directory to file
        f = open('WorkDir.ini', 'w')
        f.write(self.working_directory )
        f.close()

    def _open_files(self, mode):
        file_dialog = QtGui.QFileDialog()
        if mode == 'storm':
            title = "Open STORM files"
            extensions = "STORM coordinates (*.txt)"
            files_list = QtGui.QFileDialog.getOpenFileNames(file_dialog, title,
                                                            self.working_directory, extensions)
            for file_ in files_list:
                storm_image = StormImage(file_)
                self.storm_images_list.addItem(storm_image)
        elif mode == 'confocal':
            title = "Open Confocal files"
            # extensions = "Confocal images (*.jpg; *.png; *.tif;);;Confocal stacks (*.ics)"
            #extensions = "Confocal images (*.jpg *.png *.tif *.ics)"
            extensions = "Confocal images (*.tif" \
                         ")"
            files_list = QtGui.QFileDialog.getOpenFileNames(file_dialog, title,
                                                            self.working_directory, extensions)
            for file_ in files_list:
                confocal_image = ConfocalImage(file_)
                self.confocal_images_list.addItem(confocal_image)

    def _close_files(self, mode):
        image_list = []
        if mode == 'storm':
            image_list = self.storm_images_list
        elif mode == 'confocal':
            image_list = self.confocal_images_list
        for i in xrange(image_list.count()):
            self._close_file(mode, 0)
            # image_list.clear()

    def _close_file(self, mode, index):
        # TODO: destroy img obj
        if mode == 'storm':
            removed = self.storm_images_list.takeItem(index)
            if removed:
                self.viewer.unload_storm_image(removed)
                removed.reset_data()
                self.storm_images_list.setCurrentRow(-1)
        elif mode == 'confocal':
            removed = self.confocal_images_list.takeItem(index)
            if removed:
                self.viewer.unload_confocal_image(removed)
                removed.reset_data()
                self.confocal_images_list.setCurrentRow(-1)

    def _batch_step_files_by(self, step_size):
	#delete roi
	self.viewer.remove_roi(self.storm_roi_list.currentItem())
        storm_num = self.storm_images_list.count()
        next_active_row = self.storm_images_list.currentRow() + step_size
        if 0 <= next_active_row <= storm_num - 1:
            self.storm_images_list.setCurrentRow(next_active_row)
        else:
            if step_size > 0:
                self.storm_images_list.setCurrentRow(storm_num - 1)
            elif step_size < 0:
                self.storm_images_list.setCurrentRow(0)

        confocal_num = self.confocal_images_list.count()
        next_active_row = self.confocal_images_list.currentRow() + step_size
        if 0 <= next_active_row <= confocal_num - 1:
            self.confocal_images_list.setCurrentRow(next_active_row)
        else:
            if step_size > 0:
                self.confocal_images_list.setCurrentRow(confocal_num - 1)
            elif step_size < 0:
                self.confocal_images_list.setCurrentRow(0)

    def _close_dialog(self, dialog):
        dialog.qtDialog.close()

    def _open_dialog(self, dialog):
        # dialog.findChild(QtGui.QDialogButtonBox).clicked.connect(lambda: self.test(dialog))
        if type(dialog).__name__ == 'AnalysisDialog':
            if self.viewer.current_storm_image:
                roi = self.storm_roi_list.currentItem()
                if roi:
                    if type(roi).__name__ == 'EllipseRoi' or type(roi).__name__ == 'CircleRoi':
                        storm_data = self.viewer.display.getEllipseROIPoints(roi.roi)
                        roi_perimeter = self.viewer.display.lengthOfEllipseROI(roi.roi)
                        roi_area = self.viewer.display.areaOfEllipseROI(roi.roi)
                    elif type(roi).__name__ == 'FreehandRoi':
                        storm_data = self.viewer.display.getFreehandROIPoints(roi.roi)
                        roi_perimeter = self.viewer.display.lengthOfFreehandROI()
                        roi_area = self.viewer.display.areaOfFreehandROI()
                    elif type(roi).__name__ == 'ActiveContourRoi':
                        storm_data = self.viewer.display.getActiveContourROIPoints(roi.roi)
                        roi_perimeter = self.viewer.display.lengthOfActiveContourROI(roi.roi)
                        roi_area = self.viewer.display.areaOfActiveContourROI(roi.roi)
                    # self.show_error(message=roi_tag + ' ROI is selected. Using data selected by this ROI.')
                else:
                    storm_data = self.viewer.display.StormData_filtered
                    roi_perimeter = None
                    roi_area = None
                    # self.show_error(message='No ROI is selected. Full STORM data is used.')



                dialog.setup_analyses(
                    storm_data,
                    roi, roi_perimeter, roi_area
                )
                # set up Euclidean/confocal combobox
                if len(self.viewer.display.ConfocalMetaData) > 0:
                    dialog.setup_conf_channel(range(self.viewer.display.ConfocalMetaData['ChannelNum']),
                                         self.viewer.display.ConfocalChannelVisible)
            else:
                self.show_error(message='No STORM file is opened!')
                return False

        if type(dialog).__name__ == 'LutDialog':
            dialog.reset_channels()
            if len(self.viewer.display.StormChannelList) > 0:
                dialog.setup_channels('storm',
                    self.viewer.display.StormChannelList,
                    self.viewer.display.StormChannelVisible,
                )
            if len(self.viewer.display.ConfocalMetaData) > 0:
                dialog.setup_channels('confocal',
                    range(self.viewer.display.ConfocalMetaData['ChannelNum']),
                    self.viewer.display.ConfocalChannelVisible
                )

        if type(dialog).__name__ == 'ActiveContourDialog':
            if self.viewer.current_confocal_image:
                roi = self.storm_roi_list.currentItem()
                if roi and type(roi).__name__ == 'CircleRoi':
                    dialog.reset_channel()
                    dialog.confocal_image = self.confocal_images_list.currentItem()
                    if len(self.viewer.display.ConfocalMetaData) > 0:
                        dialog.setup_channel(
                            range(self.viewer.display.ConfocalMetaData['ChannelNum']),
                            self.viewer.display.ConfocalChannelVisible
                        )
                        dialog.setup_data(
                            self.viewer,
                            roi,
                            self.viewer.display.ConfocalZNum,
                            self.viewer.display.ConfocalOffset(),
                            self.viewer.current_confocal_image.ConfocalMetaData['SizeX']
                        )
                else:
                    self.show_error(message='Create and select a Circle ROI to use active contour evolution feature.')
                    return False
            else:
                self.show_error(message='No Confocal file is opened!')
                return False

        if type(dialog).__name__ == 'ScaleDialog':
            dialog.setup()
        if type(dialog).__name__ == 'ImageRegistrationDialog':
            #at least one channels are shwon
            if self.viewer.current_storm_image:
                if self.viewer.current_confocal_image:
                    dialog.reset_channels()
                    if len(self.viewer.display.StormChannelList) > 0:
                        dialog.setup_channels('storm',
                            self.viewer.display.StormChannelList,
                            self.viewer.display.StormChannelVisible,
                            self.viewer.display.Viewbox.ConfRegistrationChannel
                        )
                    if len(self.viewer.display.ConfocalMetaData) > 0:
                        dialog.setup_channels('confocal',
                            range(self.viewer.display.ConfocalMetaData['ChannelNum']),
                            self.viewer.display.ConfocalChannelVisible,
                            self.viewer.display.Viewbox.StormRegistrationChannel
                        )
                else:
                    self.show_error(message='No Confocal file is opened!')
                    return False
            else:
                    self.show_error(message='No STORM file is opened!')
                    return False
        dialog.qtDialog.exec_()

    def _draw_roi(self, shape):
        if self.viewer.current_storm_image:
            if len(self.viewer.current_storm_image.roi_list) > 0:
                self.viewer.remove_roi(self.storm_roi_list.currentItem())
            if shape == 'freehand':
                    self.actionDragging_mode.setChecked(False)
                    if self.actionFreehand_selecting.isChecked():
                        self.viewer.add_roi(shape)
                    else:
                        roi = self.viewer.display.addFreehandROI()
                        num = str(self.storm_settings.get_roi_counter())
                        freehand_roi = FreehandRoi('freehandROI_' + num)
                        freehand_roi.roi = roi
                        self.storm_settings.add_roi(freehand_roi)
                        self.viewer.display.ChangePanMode('Pan')
            elif shape == 'ellipse':
                    self.viewer.add_roi(shape)
            elif shape == 'circle':
                    self.viewer.add_roi(shape)
        else:
            self.actionFreehand_selecting.setChecked(False)
            self.show_error(message='No storm image is opened')

    def _export_as_image(self):
        file_dialog = QtGui.QFileDialog()
        filename = str(QtGui.QFileDialog.getSaveFileName(file_dialog, 'Save File', self.working_directory,
                                                         "PNG image file (*.png)"))
        self.viewer.display.export_as_image(filename)

    def _automatic_registration(self):
        StormOk=0
        ConfocalOk=0
        if sum(self.viewer.display.StormChannelVisible)==1:
            if sum(self.viewer.display.ConfocalChannelVisible)==1:
                autoregistration.RegisterChannels(self.viewer)
            elif sum(self.viewer.display.ConfocalChannelVisible)>1:
                self.show_error(message='More than one confocal channel is displayed')
            else:
                self.show_error(message='No Confocal channel is displayed')
        elif sum(self.viewer.display.StormChannelVisible)>1:
            self.show_error(message='More than strom one channel is displayed')
        else:
            self.show_error(message='No storm channel is displayed')

