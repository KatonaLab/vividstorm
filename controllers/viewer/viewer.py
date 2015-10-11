# -*- coding: utf-8 -*-
"""
Created on: 2015.01.26.

Author: turbo


"""

from StormDisplay import StormDisplay
from .. import default_config
from ..rois import EllipseRoi, CircleRoi, ActiveContourRoi
import os

class Viewer(object):
    def __init__(self, *args, **kwargs):
        self.main_window = kwargs['main_window']

        self.display = StormDisplay(self.main_window)
        self.init_channel_colors('storm')
        self.init_channel_colors('confocal')
        self.current_storm_image = None
        self.current_confocal_image = None

    def init_channel_colors(self, mode):
        for i in xrange(0, 4):
            color = getattr(self.main_window, 'comboBox_'+ mode + '_channel' + str(i) + '_color').currentText()
            if mode == 'storm':
                self.display.StormChannelColors[i] = default_config.channel_colors[str(color)]
            if mode == 'confocal':
                self.display.ConfocalChannelColors[i] = default_config.channel_colors[str(color)]

    def reset_all_channels_bottom_settings(self, mode):
        for i in xrange(0, 4):
            getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(i)).setEnabled(False)
            # getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(i)).setChecked(False)
            getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(i)).setText('Ch' + str(i+1))
            getattr(self.main_window, 'comboBox_'+ mode + '_channel' + str(i) + '_color').setEnabled(False)

        if mode == 'storm':
            for i in xrange(0, 4):
                getattr(self.main_window, 'label_' + mode + '_channel' + str(i) + '_info').setText('-')
        elif mode == 'confocal':
            getattr(self.main_window, 'label_' + mode + '_info').setText('-')


    def set_channel_bottom_settings(self, mode, channel_num, channel_name, text):
        getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(channel_num)).setEnabled(True)
        getattr(self.main_window, 'checkBox_'+ mode + '_channel' + str(channel_num)).setText(channel_name)
        getattr(self.main_window, 'comboBox_'+ mode + '_channel' + str(channel_num) + '_color').setEnabled(True)

        if mode == 'storm':
            getattr(self.main_window, 'label_' + mode + '_channel' + str(channel_num) + '_info').setText(text)
        elif mode == 'confocal':
            getattr(self.main_window, 'label_' + mode + '_info').setText(text)


    def show_storm_image(self, currentImage, prevImage=None):
        if currentImage:
            if self.main_window.working_directory_unset:
                if len(currentImage.file_path.split('/'))>1:
                    wd=''
                    parts=currentImage.file_path.split('/')
                    for ind in range(len(parts)-1):
                        wd+=parts[ind]+'/'
                    self.main_window.working_directory=wd
                    self.main_window.working_directory_unset=False
                elif len(currentImage.file_path.split('\\'))>1:
                    wd=''
                    parts=currentImage.file_path.split('\\')
                    for ind in range(len(parts)-1):
                        wd+=parts[ind]+'\\'
                    self.main_window.working_directory=wd
                    self.main_window.working_directory_unset=False

            self.main_window.status_bar.showMessage('Loading image, please wait...')
            self.display.DeleteStormData()
            self.reset_all_channels_bottom_settings('storm')
            if currentImage.isParsingNeeded:
                try:
                    currentImage.parse()
                except ValueError:
                    currentImage.isParsingNeeded = True
                    self.main_window.status_bar.showMessage('File format error / wrong headers used!')
                    return False

            self.current_storm_image = currentImage
            self.display.AddStormData(currentImage)

            for i, channel_name in enumerate(currentImage.StormChannelList):
                self.set_channel_bottom_settings('storm', i, channel_name,
                                                 'Points: ' + str(len(self.display.StormData_filtered[i])))

            self.main_window.storm_settings.set_rois()

            self.display.ShowAllStormChannels()
            StormFileName=''
            if self.main_window.viewer.current_storm_image!=None:
                StormFileName=str.split(self.main_window.viewer.current_storm_image.file_path,os.sep)[-1]
            ConfocalFileName='' 
            if self.main_window.viewer.current_confocal_image!=None:  
                ConfocalFileName=str.split(self.main_window.viewer.current_confocal_image.file_path,os.sep)[-1]
            self.main_window.status_bar.showMessage('Ready '+'StormFile:'+StormFileName+' ConfocalFile:'+ConfocalFileName)

    def show_confocal_image(self, currentImage, prevImage=None,ApplyButton=False):
        if currentImage:
            self.main_window.status_bar.showMessage('Loading image, please wait...')
            self.display.DeleteConfocalData()
            self.reset_all_channels_bottom_settings('confocal')
            if currentImage.isParsingNeeded:
                try:
                    currentImage.parse(self.main_window.confocal_settings.confocal_config_calibration_px, self.main_window, ApplyButton)
                except ValueError:
                    currentImage.isParsingNeeded = True
                    self.main_window.status_bar.showMessage('File format error / wrong headers used!')
                    return False           
           
            
            self.current_confocal_image = currentImage
            self.display.AddConfocalData(currentImage)

            # self.main_window.label_confocal_channel0_info.setText(str(currentImage.ConfocalMetaData))

            for i in xrange(currentImage.ConfocalMetaData['ChannelNum']):
                self.set_channel_bottom_settings('confocal', i, str(i),
                    '[All channels] ' +
                    'Pixel size: ' + str(self.display.ConfocalMetaData['SizeX']) +' | '+
                    'Z slices: ' + str(self.display.NumOfZSlices))

            self.display.ShowAllChonfocalChannels()
            StormFileName=''
            if self.main_window.viewer.current_storm_image!=None:
                StormFileName=str.split(self.main_window.viewer.current_storm_image.file_path,os.sep)[-1]
            ConfocalFileName='' 
            if self.main_window.viewer.current_confocal_image!=None:  
                ConfocalFileName=str.split(self.main_window.viewer.current_confocal_image.file_path,os.sep)[-1]
            self.main_window.status_bar.showMessage('Ready '+'StormFile:'+StormFileName+' ConfocalFile:'+ConfocalFileName)
            
    def unload_storm_image(self, image):
        if image:
            # TODO: destroy image obj
            self.current_storm_image = None
            self.reset_all_channels_bottom_settings('storm')
            # self.display.ClearPlot()
            self.main_window.storm_settings.clear_rois()
            #avoid recursion
            if  self.display.StormData != []:
                self.display.DeleteStormData()


    def unload_confocal_image(self, image):
        if image:
            # TODO: destroy image obj
            #DeleteConfocalData
            self.current_confocal_image = None
            self.reset_all_channels_bottom_settings('confocal')
            # self.display.ClearPlot()
            if  self.display.ConfocalData != []:
                self.display.DeleteConfocalData()

    def add_roi(self, shape, new_roi=None):
        if shape == 'ellipse':
            roi = self.display.addEllipseROI('ellipse')
            num = str(self.main_window.storm_settings.get_roi_counter())
            ellipse_roi = EllipseRoi('ellipseROI_' + num)
            ellipse_roi.roi = roi
            self.main_window.storm_settings.add_roi(ellipse_roi)
        elif shape == 'circle':
            roi = self.display.addEllipseROI('circle')
            num = str(self.main_window.storm_settings.get_roi_counter())
            circle_roi = CircleRoi('circleROI_' + num)
            circle_roi.roi = roi
            self.main_window.storm_settings.add_roi(circle_roi)
        elif shape == 'freehand':
            self.display.ChangePanMode('Roi')
        elif shape == 'active_contour':
            roi = self.display.createActiveContourROI(new_roi)
            num = str(self.main_window.storm_settings.get_roi_counter())
            active_contour_roi = ActiveContourRoi('activeContourROI_' + num)
            active_contour_roi.roi = roi
            self.main_window.storm_settings.add_roi(active_contour_roi)

    def remove_roi(self, roi):
        if type(roi).__name__ == 'EllipseRoi' or type(roi).__name__ == 'CircleRoi':
            self.display.deleteEllipseROI(roi.roi)
        elif type(roi).__name__ == 'FreehandRoi':
            self.display.deleteFreehandROI(roi)
        elif type(roi).__name__ == 'ActiveContourRoi':
            self.display.deleteActiveContourROI(roi.roi)
        self.main_window.storm_settings.remove_roi(self.main_window.storm_roi_list.currentRow())

    def change_drag_mode(self, is_conf):
        if is_conf:
            self.display.ChangePanMode('Conf')
        else:
            self.display.ChangePanMode('Pan')

    def set_view_mode(self, mode):
        pass

    def show_scale(self, size):
        self.display.HideScalebar()
        if size > 0:
            self.display.ShowScalebar(size)
        else:
            self.display.HideScalebar()
