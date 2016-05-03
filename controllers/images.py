# -*- coding: utf-8 -*-
"""
Created on: 2015.01.11.

Author: turbo


"""
import os
import xml.etree.ElementTree as XMLET

import numpy
from PyQt4.QtGui import QListWidgetItem
from pyqtgraph.Qt import QtGui
from PyQt4.Qt import *
from viewer import tifffile


class MicroscopeImage(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super(MicroscopeImage, self).__init__(*args, **kwargs)
        self.setText(args[0].split(os.sep)[-1])
        self.file_path = str(args[0])
        self.isParsingNeeded = True
        # self.channels = {}


class StormImage(MicroscopeImage):
    def __init__(self, *args, **kwargs):
        super(StormImage, self).__init__(*args, **kwargs)
        self.reset_data()

    def reset_data(self):
        self.StormData = []
        self.StormChannelList = []
        self.roi_list = []
        self.coords_cols = []
        self.other_cols = []


    def parse(self):
        self.isParsingNeeded = False
        # Decrease the parameters by one, because indexing goes from zero, but zeros means ignore property
        X = self.coords_cols[0] - 1
        Y = self.coords_cols[1] - 1
        Z = self.coords_cols[2] - 1
        Precision = self.other_cols[0] - 1
        ChannelName = self.other_cols[1] - 1
        Photon = self.other_cols[2] - 1
        Frame = self.other_cols[3] - 1

        # Y, Z, Precision, ChannelName, Photon, Frame
        if self.coords_cols[0] == 0 or self.coords_cols[1] == 0:
            raise Exception("X and Y values are mandatory for parsing")
        ins = open(self.file_path, "r")
        StormDataMxp = []
        FirstLine = True
        Row = 0
        self.StormChannelList = []
        try:
            for line in ins:
                l = line.strip()
                if FirstLine:
                    ContainsNumbers=False
                    LineData = l.split('\t')
                    OnlyNumberItems=0
                    for Element in LineData:
                         AllNumbers=True
                         for Char in Element:
                            #check if it is string or number
                            if Char<'0' or Char>'9':
                                 AllNumbers=False
                         if AllNumbers:
                            OnlyNumberItems+=1
                    #if more than 20 percent fo elements are number, than it is important
                    if OnlyNumberItems>(len(LineData)*0.2):
                        FirstLine = False
                if not FirstLine:
                    LineData = l.split('\t')
                    if len(LineData) == 1:
                        LineData = l.split()
                    UsefulData = []

                    UsefulData.append(LineData[X])
                    UsefulData.append(LineData[Y])
                    if Precision != -1:
                        UsefulData.append(LineData[Precision])
                    else:
                        UsefulData.append('10')

                    if Z != -1:
                        UsefulData.append(LineData[Z])
                    else:
                        UsefulData.append('0')

                    if Photon != -1:
                        UsefulData.append(LineData[Photon])
                    else:
                        UsefulData.append('-1')

                    if Frame != -1:
                        UsefulData.append(LineData[Frame])
                    else:
                        UsefulData.append('-1')
                    UsefulData.append(Row)
                    UsefulData = numpy.array(map(float, UsefulData))

                    # UsefulData[0] + 1
                    #i do not delete the last element from the line,but overwrite with the row number

                    #if we have channel name
                    if ChannelName != -1:
                        ChannelFound = 0
                        ChannelNum = 1
                        for Channel in self.StormChannelList:
                            if Channel == LineData[ChannelName]:
                                ChannelFound = ChannelNum
                            ChannelNum += 1
                        if not ChannelFound:
                            #create new channel
                            self.StormChannelList.append(LineData[ChannelName])
                            StormDataMxp.append([])
                            StormDataMxp[ChannelNum - 1].append(UsefulData)
                        else:
                            #append to the existing found channel
                            StormDataMxp[ChannelFound - 1].append(UsefulData)
                    else:
                        #append to the first channel
                        if StormDataMxp == []:
                            StormDataMxp.append([])
                            self.StormChannelList.append('STORM channel')
                        StormDataMxp[0].append(UsefulData)
                else:
                    FirstLine = False
                Row += 1
            ins.close()
            #sort the channels alphabetically
            Sortinglist=1*self.StormChannelList
            SortedList=[]
            SortedDataMxp=[]
            while Sortinglist!=[]:
                Minimal=Sortinglist[0]
                for Element in Sortinglist:
                    if Element<Minimal:
                        Minimal=Element
                #check minimal element in the original list
                index=0
                Minindex=0
                for Element in self.StormChannelList:
                    if Element==Minimal:
                        Minindex=index
                    index+=1
                SortedList.append(Minimal)
                SortedDataMxp.append(StormDataMxp[Minindex])
                Sortinglist.remove(Minimal)
            self.StormChannelList=SortedList
            self.StormData = numpy.array(SortedDataMxp)
        except ValueError:
            raise


class ConfocalImage(MicroscopeImage):
    def __init__(self, *args, **kwargs):
        super(ConfocalImage, self).__init__(*args, **kwargs)
        self.reset_data()

    def reset_data(self):
        self.ConfocalData = []
        self.ConfocalMetaData = {}

    def parse(self, calibration_px, main_window, ApplyButton=False):
        self.isParsingNeeded = False
        self.ConfocalData = []
        self.ConfocalMetaData = {}
        if calibration_px:
           self.set_calibration(calibration_px)
        with tifffile.TiffFile(self.file_path) as tif:
            # get metadata
            imageDesc = tif[0].image_description
            try:  #if we contain information in the image descriptor
                    root = XMLET.fromstring(imageDesc)
                    for L1 in root:
                        if L1.tag.split('}')[1] == 'Image':
                            for L2 in L1:
                                if L2.tag.split('}')[1] == 'Pixels':
                                    if float(L2.attrib['PhysicalSizeX']) !=1.0:
                                        self.ConfocalMetaData['SizeC'] = float(L2.attrib['SizeC'])
                                        if ApplyButton==False:
                                            self.ConfocalMetaData['SizeX'] = float(L2.attrib['PhysicalSizeX'])
                                            self.ConfocalMetaData['SizeY'] = float(L2.attrib['PhysicalSizeY'])
                                            self.ConfocalMetaData['SizeZ'] = float(L2.attrib['PhysicalSizeZ'])
                                            #set the spinbox on the GuI for the value we just read
                                            for spin_box in main_window.confocal_settings.spin_boxes:
                                               obj_name = str(spin_box.objectName())
                                               if obj_name=='doubleSpinBox_confocal_config_calibration_px':
                                                  spin_box.setValue(self.ConfocalMetaData['SizeX'])
            except:
                    pass
            #read image data
            self.ConfocalData = tif.asarray()
            # confocaldata first dimensions z channel, color channels, than data
            ConfShape = self.ConfocalData.shape
            ConfDim = len(self.ConfocalData.shape)
            if ConfDim == 4:
                self.ConfocalMetaData['ChannelNum'] = int(ConfShape[1])
            if ConfDim == 3:
                if 'SizeC' in self.ConfocalMetaData:
                    self.ConfocalMetaData['ChannelNum'] = int(self.ConfocalMetaData['SizeC'])
                else:
                    self.ConfocalMetaData['ChannelNum'] = 1
            if ConfDim == 2:
                self.ConfocalMetaData['ChannelNum'] = 1
            #set the z channel to the middle of the stacks
            NumOfZSlices=0
            # more Zchannels and color channels
            if len(self.ConfocalData.shape) > 3:
                    NumOfZSlices=self.ConfocalData.shape[0]           
            elif len(self.ConfocalData.shape) > 2 and self.ConfocalMetaData['ChannelNum'] == 1:
                    #z channels only
                    NumOfZSlices=self.ConfocalData.shape[0]       
            elif len(self.ConfocalData.shape) > 2 and self.ConfocalMetaData['ChannelNum'] > 1:
                    #color channels only
                    NumOfZSlices=1
            else:
                    #a single tif image
                    NumOfZSlices=1
            if ApplyButton==False: 
                for spin_box in main_window.confocal_settings.spin_boxes:
                    obj_name = str(spin_box.objectName())
                    if obj_name=='spinBox_confocal_display_appear_zposition':
                       spin_box.setValue(round(float(NumOfZSlices-1)/2.0)+1)
                main_window.viewer.display.ConfocalZNum=round(float(NumOfZSlices-1)/2.0)


    def set_calibration(self, px):
        self.ConfocalMetaData['SizeX'] = px
        self.ConfocalMetaData['SizeY'] = px
        self.ConfocalMetaData['SizeZ'] = px
