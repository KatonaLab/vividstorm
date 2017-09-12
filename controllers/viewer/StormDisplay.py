# -*- coding: utf-8 -*-
"""
VividSTORM imageDisplay
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import pyqtgraph.exporters
import numpy as np
from PyQt5.QtGui import *
import math
from . import CustomViewBox
from . import StormLUT
from .. import default_config
import scipy.ndimage
import os
from . import ConfocalLUT
import gc
import copy
import numpy
import sys
import matplotlib.pyplot as plt


class StormDisplay(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.StormData = []
        self.StormData_filtered = []
        self.StormChannelList = []
        self.ConfocalImage=[]
        self.DisplayedStormChannel = [0, 0, 0, 0]  # this is a pointer to the image
        self.StormChannelVisible = [False, False, False, False]
        self.StormChannelColors = [(), (), (), ()]

        self.ConfocalData = []
        self.ConfocalMetaData = {}
        self.ConfChannelToShow = []

        self.StormLUTTickValues = [[0, 0.5], [0, 0.5], [0, 0.5], [0, 0.5]]
        self.ConfocalLUTTickValues = [[0, 1], [0, 1], [0, 1], [0, 1]]

        self.ConfocalInterpolationMethod = 3  # 0 nearest neighbour 1 bilinear 2 square 3 cubic
        self.DisplayedConfocalChannel = [0, 0, 0, 0]  # this is a pointer to the image
        self.ConfocalChannelVisible = [False, False, False, False]
        self.ConfocalChannelColors = [(), (), (), ()]
        self.ConfocalTransparency = 0.8
        self.StormTransparency = 0.5
        self.StormZColoring = False

        self.ConfocalSizeMultiplier = 1.0

        self.plot_widget = QWidget()
        self.Viewbox = []

        self.ScaleBar = []
        self.ScaleText = []
        self.ConfocalZNum = 0
        self.NumOfZSlices = 0

        self.ConfocalLUTWidget = []
        self.StormLutImages = [0, 0, 0, 0]
        self.init_widget()

        self.storm_dot_size=[]

    def ChangePanMode(self, Mode):
        self.Viewbox.PanMode = Mode

    def filter_data(self, data):
        return self.main_window.storm_settings.filter_storm_data(data)

    def SetConfocalInterpolationMethod(self, method_string):
        IPMethod = 0
        if method_string == 'nearest':
            IPMethod = 0
        elif method_string == 'bilinear':
            IPMethod = 1
        elif method_string == 'sqare':
            IPMethod = 2
        elif method_string == 'cubic':
            IPMethod = 3
        self.ConfocalInterpolationMethod = IPMethod

    def AddStormData(self, storm_image):
        self.StormData = storm_image.StormData
        self.StormData_filtered = self.filter_data(self.StormData)
        self.StormChannelList = storm_image.StormChannelList
        channels= [str(self.main_window.comboBox_storm_filter_ROI_channel.currentText())]
        #if we have roi filter switched on and we have a roi - filter the points
        if self.main_window.groupBox_storm_filter_ROI.isChecked():
            roi = self.main_window.storm_roi_list.currentItem()
            if roi:
                if type(roi).__name__ == 'EllipseRoi' or type(roi).__name__ == 'CircleRoi':
                   self.StormData_filtered = self.filterROIPoints(roi.roi,'Circle',channels)
                elif type(roi).__name__ == 'FreehandRoi':
                   self.StormData_filtered = self.filterROIPoints( roi.roi,'Freehand',channels)
                elif type(roi).__name__ == 'ActiveContourRoi':
                    self.StormData_filtered = self.filterROIPoints(roi.roi,'Activecontour',channels)



    def SetStormChannelVisible(self, ChannelNumber, Visible):
        self.StormChannelVisible[ChannelNumber] = Visible
        #set the dropdown menu items for visible channels:
        while self.main_window.comboBox_storm_filter_ROI_channel.count() > 0:
            self.main_window.comboBox_storm_filter_ROI_channel.removeItem(0)
        index=0
        for V in self.StormChannelVisible:
            if V:
                self.main_window.comboBox_storm_filter_ROI_channel.addItem(self.StormChannelList[index])
            index+=1

        self.ShowAll()

    def SetStormChannelColor(self, ChannelNumber, Color):
        self.StormChannelColors[ChannelNumber] = default_config.channel_colors[Color]
        if self.StormChannelVisible[ChannelNumber]:
            self.ShowAll()

    def SetConfocalChannelVisible(self, ChannelNumber, Visible):
        self.ConfocalChannelVisible[ChannelNumber] = Visible
        self.ShowAll()

    def SetConfocalChannelColor(self, ChannelNumber, Color):
        self.ConfocalChannelColors[ChannelNumber] = default_config.channel_colors[Color]
        if self.ConfocalChannelVisible[ChannelNumber]:
            self.ShowAll()

    def DeleteStormData(self):
        for StormCh in self.DisplayedStormChannel:
            if StormCh!=0:
                self.Viewbox.removeItem(StormCh)
        for R in self.Viewbox.StormMarkerRois:
                self.plot_widget.removeItem(R)
        self.Viewbox.StormMarkerRois = []
        self.StormData = []
        self.StormData_filtered = []
        self.StormChannelList = []
        self.DisplayedStormChannel = [0, 0, 0, 0]
        try:
            self.plot_widget.clear()
        except:
            pass
        self.ShowAll()


    def ClearAll(self):
        self.plot_widget.clear()
        self.DisplayedStormChannel = [0, 0, 0, 0]
        self.DisplayedConfocalChannel = [0, 0, 0, 0]

    def ClearPlot(self):
        #clear only the channels,not the ROI or other elements
        for ConfCh in self.DisplayedConfocalChannel:
            if ConfCh!=0:
                self.Viewbox.removeItem(ConfCh)
        for StormCh in self.DisplayedStormChannel:
            if StormCh!=0:
                self.Viewbox.removeItem(StormCh)
        self.DisplayedStormChannel = [0, 0, 0, 0]
        self.DisplayedConfocalChannel = [0, 0, 0, 0]

    def AddConfocalData(self, confocal_image):
        self.ConfocalSizeMultiplier=1.0
        self.ConfocalData = copy.deepcopy(confocal_image.ConfocalData)
        self.ConfocalMetaData = copy.deepcopy(confocal_image.ConfocalMetaData)
        self.NumOfZSlices=0
        ConfocalDataThreshold=1000 # threshold for confocal data above which it shouldn't be resized 10x
        # more Zchannels and color channels
        if len(self.ConfocalData.shape) > 3:
            Channels = self.ConfocalData[self.ConfocalZNum, :, :, :]
            self.NumOfZSlices=self.ConfocalData.shape[0]
            if self.ConfocalData.shape[2]>ConfocalDataThreshold:
                self.ConfocalSizeMultiplier=1.0
            self.ConfChannelToShow = np.zeros(
                (self.ConfocalData.shape[1], self.ConfocalData.shape[2] *  self.ConfocalSizeMultiplier, self.ConfocalData.shape[3] *  self.ConfocalSizeMultiplier))
            for i in range(self.ConfocalData.shape[1]):
                self.ConfChannelToShow[i, :, :] = scipy.ndimage.zoom(Channels[i, :, :],  self.ConfocalSizeMultiplier,
                                                                     order=self.ConfocalInterpolationMethod)
        elif len(self.ConfocalData.shape) > 2 and self.ConfocalMetaData['ChannelNum'] == 1:
            #z channels only
            if self.ConfocalData.shape[1]>ConfocalDataThreshold:
                self.ConfocalSizeMultiplier=1.0
            self.ConfChannelToShow = np.zeros((1, self.ConfocalData.shape[1] *  self.ConfocalSizeMultiplier, self.ConfocalData.shape[2] *  self.ConfocalSizeMultiplier))
            self.NumOfZSlices=self.ConfocalData.shape[0]
            if self.ConfocalData.shape[0]<=self.ConfocalZNum:
                self.ConfocalZNum=int(self.ConfocalData.shape[0]/2)
            self.ConfChannelToShow[0, :, :] = scipy.ndimage.zoom(self.ConfocalData[self.ConfocalZNum, :, :],  self.ConfocalSizeMultiplier,
                                                                 order=self.ConfocalInterpolationMethod)
        elif len(self.ConfocalData.shape) > 2 and self.ConfocalMetaData['ChannelNum'] > 1:
            #color channels only
            if self.ConfocalData.shape[1]>ConfocalDataThreshold:
                self.ConfocalSizeMultiplier=1.0
            size_tuple = (self.ConfocalData.shape[0], int(self.ConfocalData.shape[1] * self.ConfocalSizeMultiplier), int(self.ConfocalData.shape[2] * self.ConfocalSizeMultiplier))
            self.ConfChannelToShow = np.zeros(size_tuple)
            for i in range(self.ConfocalData.shape[0]):
                self.ConfChannelToShow[i, :, :] = scipy.ndimage.zoom(self.ConfocalData[i, :, :],  self.ConfocalSizeMultiplier,
                                                                     order=self.ConfocalInterpolationMethod)
        else:
            #a single tif image
            if self.ConfocalData.shape[0]>ConfocalDataThreshold:
                self.ConfocalSizeMultiplier=1.0
            self.ConfChannelToShow = np.zeros((1, int(self.ConfocalData.shape[0] * self.ConfocalSizeMultiplier), int(self.ConfocalData.shape[1] * self.ConfocalSizeMultiplier)))
            self.ConfChannelToShow[0, :, :] = scipy.ndimage.zoom(self.ConfocalData,  self.ConfocalSizeMultiplier,
                                                                 order=self.ConfocalInterpolationMethod)
        # print(self.ConfocalSizeMultiplier)

    def DeleteConfocalData(self):
        if self.Viewbox != []:
            self.Viewbox.deleteConfocalImage()
            for R in self.Viewbox.ConfMarkerRois:
                self.plot_widget.removeItem(R)
            self.Viewbox.ConfMarkerRois = []
            self.Viewbox.AffineTransform = []
        for ConfCh in self.DisplayedConfocalChannel:
            if ConfCh!=0:
                self.Viewbox.removeItem(ConfCh)
        if self.ConfocalImage!=[]:
            self.ConfocalImage.reset_data()
        self.ConfocalMetaData = {}
        self.DisplayedConfocalChannel[:]
        for a in self.DisplayedConfocalChannel:
            del a
        del self.DisplayedConfocalChannel[:]
        del self.DisplayedConfocalChannel
        self.DisplayedConfocalChannel = [0, 0, 0, 0]
        self.ConfChannelToShow = []
        self.ConfocalSizeMultiplier=1.0
        del self.ConfocalData
        self.ConfocalData = []
        self.main_window.viewer.unload_confocal_image(True)
        try:
            self.plot_widget.clear()
        except:
            pass
        gc.collect()
        gc.collect()
        self.ShowAll()


    def ShowAll(self):
        self.main_window.status_bar.showMessage('Recalculating image, please wait...')
        self.ClearPlot()
        self.ShowAllStormChannels()
        self.ShowAllConfocalChannels()
        StormFileName=''
        if self.main_window.viewer.current_storm_image!=None:
                StormFileName=str.split(self.main_window.viewer.current_storm_image.file_path,os.sep)[-1]
        ConfocalFileName=''
        if self.main_window.viewer.current_confocal_image!=None:
                ConfocalFileName=str.split(self.main_window.viewer.current_confocal_image.file_path,os.sep)[-1]
        self.main_window.status_bar.showMessage('Ready '+'StormFile:'+StormFileName+' ConfocalFile:'+ConfocalFileName)

    def export_as_image(self, file_path):
        exporter = pg.exporters.ImageExporter(self.plot_widget.getPlotItem())
        # exporter.parameters()['width'] = 100   # (note this also affects height parameter)
        exporter.export(file_path)

    def init_widget(self):
        # create new qt app
        # create userdefined viewbox with our own mouse events
        self.Viewbox = CustomViewBox.CustomViewBox(lockAspect=True, invertY=True)
        self.Viewbox.main_window = self.main_window
        self.plot_widget = pg.PlotWidget(viewBox=self.Viewbox, lockAspect=True, enableMenu=True)
        # self.plot_widget = pg.PlotWidget()
        self.Viewbox.setWindow(self.plot_widget)
        # !!! no mouse event at the moment
        # self.main_window.viewer_container_layout.removeWidget(self.plot_widget)
        # self.plot_widget.close()
        self.plot_widget.resize(600, 600)
        self.main_window.viewer_container_layout.addWidget(self.plot_widget)
        self.plot_widget.show()

    def ConfocalOffset(self):
        if self.Viewbox != []:
            return self.Viewbox.ConfocalOffset
        return [0, 0]

    def ShowScalebar(self, Size):
        if self.ScaleBar == []:
            ViewRange = self.plot_widget.viewRange()
            XLength = (ViewRange[0][1] - ViewRange[0][0]) * 0.05
            YLength = (ViewRange[1][1] - ViewRange[1][0]) * 0.05
            Xpos = ViewRange[0][0] + XLength
            Ypos = ViewRange[0][0] + YLength
            self.ScaleBar = self.plot_widget.plot(x=[Xpos, Xpos + Size], y=[Ypos, Ypos], symbol='o')
            PosX = Xpos
            PosY = Ypos + YLength * 0.1
            self.ScaleText = pg.TextItem(text=str(Size) + ' nm', color=(200, 200, 200))
            self.plot_widget.addItem(self.ScaleText)
            self.ScaleText.setPos(PosX, PosY)
            self.Viewbox.setScaleBar(self.ScaleBar, self.plot_widget, Size, self.ScaleText)
            self.Viewbox.updateMatrix()

    def HideScalebar(self):
        self.Viewbox.deleteScaleBar()
        self.ScaleBar = []
        self.ScaleText = []

    def addFreehandROI(self):
        return pg.QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(self.Viewbox.FreehandRoi))

    def createActiveContourROI(self, PointList=[[0, 0], [0, 3000.2], [3000, 3000], [3000, 0]]):
        # PointList coordinates of point as x,y. Ex: [[0,0], [5,4], [3,2] ....]
        QtPoints = []
        DrawnElements = []
        FirstTime = True
        for PP in PointList:
            QtPoints.append(pg.Point(PP))
            if FirstTime:
                FirstTime = False
                FirstPoint = PP
            else:
                r1 = pg.QtGui.QGraphicsLineItem(PrevPoint[0], PrevPoint[1], PP[0], PP[1])
                r1.setPen(pg.mkPen('w'))
                DrawnElements.append(r1)
                self.Viewbox.addItem(r1)
            PrevPoint = PP
        #closing the roi
        QtPoints.append(pg.Point(FirstPoint))
        r1 = pg.QtGui.QGraphicsLineItem(PP[0], PP[1], FirstPoint[0], FirstPoint[1], )
        r1.setPen(pg.mkPen('w'))
        DrawnElements.append(r1)
        self.Viewbox.addItem(r1)
        return [pg.QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(QtPoints)), QtPoints, DrawnElements]

    def GetEdgeCoords(self, matrix):
        edgecoords = []
        outmatrix = numpy.copy(matrix)

        for x in range(numpy.shape(matrix)[0]):
            for y in range(numpy.shape(matrix)[1]):
                if matrix[x, y] == 1:
                    nn = self.CountNeighborNumber(x, y, matrix)
                    if nn > 0:

                        edgecoords.append([x, y])
                    else:
                        outmatrix[x, y] = 0

        return [edgecoords, outmatrix]

    def CountNeighborNumber(self, x, y, matrix):
        nn = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if matrix[x + i, y + j] == 0:
                        nn += 1
                except:
                    nn +=1
        return nn

    def matrix_order(self, edgecoords):
        ACROI=[]
        CurrentPoint = edgecoords[0]
        ACROI.append(CurrentPoint)
        PointAdded = True
        while PointAdded:
            PointAdded=False
            NeighbouringPoints=0
            MinDist=2
            MinPoint=[]
            for point in edgecoords:
                if math.fabs(CurrentPoint[0]-point[0])<2 and math.fabs(CurrentPoint[1]-point[1])<2:
                    Dist=math.sqrt((CurrentPoint[0]-point[0])*(CurrentPoint[0]-point[0])+(CurrentPoint[1]-point[1])
                                       *(CurrentPoint[1]-point[1]))
                    if Dist<MinDist and Dist!=0:
                        MinDist=Dist
                        MinPoint=point
            if MinPoint!=[]:
                PointAdded=True
                edgecoords.remove(MinPoint)
                ACROI.append(MinPoint)
                CurrentPoint=MinPoint
        zoom =1000.0 * self.ConfocalMetaData['SizeX']
        for i in range(len(ACROI)):
            ACROI[i] = [ACROI[i][1] * 1000.0 * self.ConfocalMetaData['SizeY'] + self.ConfocalOffset()[1] * 100.0 * self.ConfocalMetaData['SizeY'] + zoom / 2.0,
                        ACROI[i][0] * 1000.0 * self.ConfocalMetaData['SizeX'] + self.ConfocalOffset()[0] * 100.0 * self.ConfocalMetaData['SizeX'] + zoom / 2.0]#zoom
        return ACROI

    def createActiveContourROI_3d(self, PointList):
        # PointList coordinates of point as x,y. Ex: [[0,0], [5,4], [3,2] ....]

        [edgecoords, outroi] = self.GetEdgeCoords(PointList[7])
        xy_pointlist = self.matrix_order(edgecoords)
        QtPoints = []
        DrawnElements = []
        FirstTime = True
        for PP in xy_pointlist:
            QtPoints.append(pg.Point(PP))
            if FirstTime:
                FirstTime = False
                FirstPoint = PP
            else:
                r1 = pg.QtGui.QGraphicsLineItem(PrevPoint[0], PrevPoint[1], PP[0], PP[1])
                r1.setPen(pg.mkPen('w'))
                DrawnElements.append(r1)
                self.Viewbox.addItem(r1)
            PrevPoint = PP
        #closing the roi
        QtPoints.append(pg.Point(FirstPoint))
        r1 = pg.QtGui.QGraphicsLineItem(PP[0], PP[1], FirstPoint[0], FirstPoint[1], )
        r1.setPen(pg.mkPen('w'))
        DrawnElements.append(r1)
        self.Viewbox.addItem(r1)
        return [pg.QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(QtPoints)), QtPoints, DrawnElements]

    def lengthOfActiveContourROI(self, roi):
        # this QtPoints parameter is the second return value of the createActiveContourROI function
        RoiCorners = roi[1]
        n = len(RoiCorners)  # of corners
        length = 0.0
        for i in range(n):
            j = (i + 1) % n
            XDif = (RoiCorners[i].x() - RoiCorners[j].x())
            YDif = (RoiCorners[i].y() - RoiCorners[j].y())
            length += math.sqrt(XDif * XDif + YDif * YDif)
        return length

    def areaOfActiveContourROI(self, roi):
        # this QtPoints parameter is the second return value of the createActiveContourROI function
        #shoelace formula
        RoiCorners = roi[1]
        n = len(RoiCorners)  # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += RoiCorners[i].x() * RoiCorners[j].y()
            area -= RoiCorners[j].x() * RoiCorners[i].y()
        area = abs(area) / 2.0
        return area

    def deleteActiveContourROI(self, roi):
        # this parameter is the third return value of the createActiveContourROI function
        self.Viewbox.deleteActiveContourROI(roi[2])

    def deleteActiveContourROI3d(self, roi):
        # this parameter is the third return value of the createActiveContourROI function
        self.Viewbox.deleteActiveContourROI3d(roi[2])

    def filterROIPoints(self, roi,roitype,channels):
        if roitype=='Activecontour':
            PolygonItem = roi[0]
            roiShape = PolygonItem.shape()
        elif roitype=='Freehand':
            roiShape = roi.shape()
        elif roitype=='Circle':
            roiShape = roi.mapToParent(roi.shape())
        ROIPoints = []
        ChannelNum = len(self.StormChannelList)
        #for all channels
        for i in range(ChannelNum):
                ROIPoints.append([])
                FilteredChannel=False
                for ch in channels:
                    if ch==self.StormChannelList[i]:
                        FilteredChannel=True
                if FilteredChannel:
                        Data = self.StormData_filtered[i]
                        #if the ROI contains the point
                        for Point in Data:
                            if roiShape.contains(pg.Point(Point[0], Point[1])):
                                ROIPoints[-1].append(Point)
                else:
                    if self.StormChannelVisible[i]:
                        ROIPoints[-1]=self.StormData_filtered[i]
        return ROIPoints

    def getActiveContourROIPoints(self, roi):
        # this roi parameter should be the first return value 'pg.QtGui.QGraphicsPolygonItem(QtGui.QPolygonF(QtPoints))' of the createActiveContourROI function
        PolygonItem = roi[0]
        ROIPoints = []
        roiShape = PolygonItem.shape()
        ChannelNum = len(self.StormChannelList)
        #for all cahnnels
        for i in range(ChannelNum):
            if self.StormChannelVisible[i]:
                ROIPoints.append([])
                # Data = self.StormData[i]
                Data = self.StormData_filtered[i]
                #if the ROI contains the point
                for Point in Data:
                    if roiShape.contains(pg.Point(Point[0], Point[1])):
                        ROIPoints[-1].append(Point)
        return ROIPoints


    def deleteFreehandROI(self, roi):
        self.Viewbox.deleteFreehandROI(roi)

    def lengthOfFreehandROI(self):
        RoiCorners = self.Viewbox.FreehandRoi
        n = len(RoiCorners)  # of corners
        length = 0.0
        for i in range(n):
            j = (i + 1) % n
            XDif = (RoiCorners[i].x() - RoiCorners[j].x())
            YDif = (RoiCorners[i].y() - RoiCorners[j].y())
            length += math.sqrt(XDif * XDif + YDif * YDif)
        return length

    def areaOfFreehandROI(self):
        # shoelace formula
        RoiCorners = self.Viewbox.FreehandRoi
        n = len(RoiCorners)  # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += RoiCorners[i].x() * RoiCorners[j].y()
            area -= RoiCorners[j].x() * RoiCorners[i].y()
        area = abs(area) / 2.0
        return area


    def getFreehandROIPoints(self, roi):
        ROIPoints = []
        roiShape = roi.shape()
        ChannelNum = len(self.StormChannelList)
        # for all cahnnels
        for i in range(ChannelNum):
            if self.StormChannelVisible[i]:
                ROIPoints.append([])
                # Data = self.StormData[i]
                Data = self.StormData_filtered[i]
                #if the ROI contains the point
                for Point in Data:
                    if roiShape.contains(pg.Point(Point[0], Point[1])):
                        ROIPoints[-1].append(Point)
        return ROIPoints

    def addEllipseROI(self, shape):
        # ROI is 10% of the image
        ViewRange = self.plot_widget.viewRange()
        XLength = (ViewRange[0][1] - ViewRange[0][0]) * 0.1
        YLength = (ViewRange[1][1] - ViewRange[1][0]) * 0.1
        Xpos = (ViewRange[0][1] + ViewRange[0][0]) / 2
        Ypos = (ViewRange[1][0] + ViewRange[1][1]) / 2
        if shape == 'ellipse':
            roi = pg.EllipseROI([Xpos, Ypos], [XLength, YLength])
        elif shape == 'circle':
            roi = pg.CircleROI([Xpos, Ypos], [XLength, XLength])
        self.plot_widget.addItem(roi)
        return roi

    def getPixelIntensityInRoi(self, roi, roitype, offset):

        img=self.ConfChannelToShow
        #print(img.shape)


        zoomout=1.0/self.main_window.viewer.display.ConfocalSizeMultiplier
        resizedim=scipy.ndimage.zoom(img,(1,zoomout,zoomout),order=0)
        #print(resizedim.shape)

        PixelsXX=[]
        PixelsYY=[]
        if roitype=='Activecontour':
            PolygonItem = roi[0]
            roiShape = PolygonItem.shape()
        elif roitype=='Freehand':
            roiShape = roi.shape()
        elif roitype=='Circle':
            roiShape = roi.mapToParent(roi.shape())
        elif roitype=='Ellipse':
            roiShape = roi.mapToParent(roi.shape())

        offset[0]=offset[0]*1000.0*self.ConfocalMetaData['SizeX']
        offset[1]=offset[1]*1000.0*self.ConfocalMetaData['SizeX']
        for ii in range(resizedim.shape[1]):
            for jj in range(resizedim.shape[2]):
                Scale=1000.0
                if roiShape.contains(pg.Point(int((ii+0.5)*Scale * self.ConfocalMetaData['SizeX']+offset[0]), int((jj+0.5)*Scale * self.ConfocalMetaData['SizeX']+offset[1]) )):
                    PixelsXX.append(ii)
                    PixelsYY.append(jj)

        NumPixelss=len(PixelsXX)
        Intensitiess=[]
        for chh in range(resizedim.shape[0]):
            # calculate pixelpoint back to display point
            SumIntensity=0.0
            for ind in range(NumPixelss):
                SumIntensity+=resizedim[chh,PixelsYY[ind],PixelsXX[ind]]
            Intensitiess.append(SumIntensity)
        #print(NumPixelss)

        return [Intensitiess,NumPixelss]


    def areaOfEllipseROI(self, roi):
        return math.pi * roi.size().x()/2 * roi.size().y()/2

    def lengthOfEllipseROI(self, roi):
        roiShape = roi.mapToParent(roi.shape())
        return roiShape.length()

    def deleteEllipseROI(self, roi):
        self.Viewbox.deleteEllipseROI(roi)
        roi = None

    def getEllipseROIPoints(self, roi):
        ROIPoints = []
        # shape the ROi for the view
        roiShape = roi.mapToParent(roi.shape())

        ChannelNum = len(self.StormChannelList)
        # for all channels
        for i in range(ChannelNum):
            if self.StormChannelVisible[i]:
                ROIPoints.append([])
                # Data = self.StormData[i]
                Data = self.StormData_filtered[i]
                #if the ROI contains the point
                for Point in Data:
                    if roiShape.contains(pg.Point(Point[0], Point[1])):
                        ROIPoints[-1].append(Point)
        return ROIPoints

    def ShowAllChonfocalChannels(self):
        for ChannelNum in range(self.ConfocalMetaData['ChannelNum']):
            self.ShowConfocalChannel(ChannelNum)

    def ShowConfocalChannel(self, ChannelNum):
        if type(self.ConfocalData).__name__ != 'list':
            if ChannelNum > 3:
                ChannelNum = 3
            if self.ConfocalChannelVisible[ChannelNum] == True:
                self.DisplayedConfocalChannel[ChannelNum] = pg.ImageItem(self.ConfChannelToShow[ChannelNum],
                                                                         opacity=self.ConfocalTransparency,
                                                                         compositionMode=pg.QtGui.QPainter.CompositionMode_Plus)
                self.DisplayedConfocalChannel[ChannelNum].rotate(90)
                self.DisplayedConfocalChannel[ChannelNum].scale(1.0, -1.0)
                # other compositon mode:QtGui.QPainter.CompositionMode_Multiply QtGui.QPainter.CompositionMode_Overlay
                Scale=1000.0/self.ConfocalSizeMultiplier
                self.DisplayedConfocalChannel[ChannelNum].scale(Scale * self.ConfocalMetaData['SizeX'],
                                                                Scale * self.ConfocalMetaData['SizeY'])
                Offset = self.ConfocalOffset()
                self.DisplayedConfocalChannel[ChannelNum].translate(Offset[0], Offset[1])
                self.DisplayedConfocalChannel[ChannelNum].setZValue(-1)
                self.Viewbox.setConfocalImage(self, ChannelNum)
                # set color of the image:
                pos = np.array([self.ConfocalLUTTickValues[ChannelNum][0], self.ConfocalLUTTickValues[ChannelNum][1]])
                color = np.array([[0, 0, 0, 255], [self.ConfocalChannelColors[ChannelNum][0],
                                                   self.ConfocalChannelColors[ChannelNum][1],
                                                   self.ConfocalChannelColors[ChannelNum][2], 255]], dtype=np.ubyte)
                map = pg.ColorMap(pos, color)
                ColorLut = map.getLookupTable(0.0, 1.0, 256)

                self.DisplayedConfocalChannel[ChannelNum].setLookupTable(ColorLut)
                self.plot_widget.addItem(self.DisplayedConfocalChannel[ChannelNum])


    def ShowConfocalLut(self, ChannelNumber, ChannelColor):
        if self.DisplayedConfocalChannel != []:
            if self.DisplayedConfocalChannel[ChannelNumber] != 0:
                container = self.main_window.dialog_tool_lut.verticalLayout_confocal_lut
                for i in reversed(range(container.count())):
                    container.itemAt(i).widget().setParent(None)

                self.ConfocalLUTWidget = pg.GraphicsWindow()
                self.main_window.dialog_tool_lut.verticalLayout_confocal_lut.addWidget(self.ConfocalLUTWidget)

                LowerSpin=self.main_window.dialog_tool_lut.spinBox_confocal_LUT_lower
                UpperSpin=self.main_window.dialog_tool_lut.spinBox_confocal_LUT_upper
                self.main_window.dialog_tool_lut.spinBox_confocal_LUT_lower.setValue(self.ConfocalLUTTickValues[ChannelNumber][0]*100)
                self.main_window.dialog_tool_lut.spinBox_confocal_LUT_upper.setValue(self.ConfocalLUTTickValues[ChannelNumber][1]*100)
                grad = ConfocalLUT.GradientEditorItem(self, ChannelNumber, LowerSpin, UpperSpin, orientation='top', )
                C0 = ChannelColor[0]
                C1 = ChannelColor[1]
                C2 = ChannelColor[2]
                gradcolors = {'ticks': [(0.0, (0, 0, 0, 255)), (1.0, (C0, C1, C2, 255))], 'mode': 'rgb'}
                grad.restoreState(gradcolors)
                grad.setTickValue(grad.listTicks()[0][0], self.ConfocalLUTTickValues[ChannelNumber][0])
                grad.setTickValue(grad.listTicks()[1][0], self.ConfocalLUTTickValues[ChannelNumber][1])
                grad.updateGradient()
                self.ConfocalLUTWidget.addItem(grad, 0, 0)

                h =  self.DisplayedConfocalChannel[ChannelNumber].getHistogram()
                for d in range(len(h[1])):
                    if h[1][d]>0:
                        h[1][d]=math.log(h[1][d])
                curve = pg.PlotCurveItem(h[0],h[1], fillLevel=0, brush=(0, 0, 255, 80))

                plt1 = self.ConfocalLUTWidget.addPlot(1, 0)
                plt1.addItem(curve)

                plt1.setLogMode(False,True)

                #plt1.setXRange(MinIntensity, MaxIntensity)





    def setConfocalLUTTickValues(self, ChannelNumber, Values):
        self.ConfocalLUTTickValues[ChannelNumber] = Values

    def ShowStormLut(self, ChannelNumber, ChannelColor):
        if self.DisplayedStormChannel != []:
            container = self.main_window.dialog_tool_lut.verticalLayout_storm_lut
            for i in reversed(range(container.count())):
                container.itemAt(i).widget().setParent(None)

            # self.StormLUTWidget = pg.PlotWidget()
            self.StormLUTWidget = pg.GraphicsWindow()
            self.main_window.dialog_tool_lut.verticalLayout_storm_lut.addWidget(self.StormLUTWidget)

            LowerSpin=self.main_window.dialog_tool_lut.spinBox_storm_LUT_lower
            UpperSpin=self.main_window.dialog_tool_lut.spinBox_storm_LUT_upper
            self.main_window.dialog_tool_lut.spinBox_storm_LUT_lower.setValue(self.StormLUTTickValues[ChannelNumber][0]*100)
            self.main_window.dialog_tool_lut.spinBox_storm_LUT_upper.setValue(self.StormLUTTickValues[ChannelNumber][1]*100)
            grad = StormLUT.GradientEditorItem(self, ChannelNumber,LowerSpin,UpperSpin, orientation='top')
            C0 = ChannelColor[0]
            C1 = ChannelColor[1]
            C2 = ChannelColor[2]
            gradcolors = {'ticks': [(0.0, (0, 0, 0, 255)), (1.0, (C0, C1, C2, 255))], 'mode': 'rgb'}
            grad.restoreState(gradcolors)
            grad.setTickValue(grad.listTicks()[0][0], self.StormLUTTickValues[ChannelNumber][0])
            grad.setTickValue(grad.listTicks()[1][0], self.StormLUTTickValues[ChannelNumber][1])
            grad.updateGradient()
            self.StormLUTWidget.addItem(grad, 0, 0)

            Gausses = np.array(self.StormData_filtered[ChannelNumber])
            if self.StormZColoring == True:
                Intensity = Gausses[:, 3]
                Intensity = Intensity - np.amin(Intensity) + 0.1
            else:
                Intensity = Gausses[:, 2]
            MaxIntensity = np.amax(Intensity)
            MinIntensity = np.amin(Intensity)
            y, x = np.histogram(Intensity, bins=np.linspace(MinIntensity, MaxIntensity, 200))
            curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
            plt1 = self.StormLUTWidget.addPlot(1, 0)
            plt1.addItem(curve)
            plt1.setXRange(MinIntensity, MaxIntensity)
            self.UpdateStormChannel(ChannelNumber, self.StormLUTTickValues[ChannelNumber])

    def UpdateConfocalChannel(self, ChannelNum, LutPositions):
        self.ConfocalLUTTickValues[ChannelNum] = LutPositions
        pos = np.array([self.ConfocalLUTTickValues[ChannelNum][0], self.ConfocalLUTTickValues[ChannelNum][1]])
        color = np.array([[0, 0, 0, 255], [self.ConfocalChannelColors[ChannelNum][0],
                                                   self.ConfocalChannelColors[ChannelNum][1],
                                                   self.ConfocalChannelColors[ChannelNum][2], 255]], dtype=np.ubyte)
        map = pg.ColorMap(pos, color)
        ColorLut = map.getLookupTable(0.0, 1.0, 256)

        self.DisplayedConfocalChannel[ChannelNum].setLookupTable(ColorLut)


    def UpdateStormChannel(self, ChannelNumber, LutPositions):
        self.StormLUTTickValues[ChannelNumber] = LutPositions
        Gausses = np.array(self.StormData_filtered[ChannelNumber])
        XCoords = []
        YCoords = []
        DrawTogether=False
        if self.StormZColoring == True:
            Intensity = Gausses[:, 3]
            Intensity = Intensity - np.amin(Intensity) + 0.1
            Intensity = Intensity / np.amax(Intensity)
        else:
            Intensity = Gausses[:, 2]
            if all( Intensity==Intensity[0])or self.main_window.groupBox_storm_config_display.isChecked():
                    DrawTogether=True
            # else:    #
            Intensity = 25.0 / (Gausses[:, 2]**2) #
            #Intensity = Intensity / np.amax(Intensity)
        # Prec = Gausses[:, 2]
        # Prec = Prec / np.amax(Prec)
        # Sigma = 1.0 / (np.sqrt(2 * np.pi) * Prec)

        #Sizes = Sigma * self.storm_dot_size*2.5  # five
        Sizes= Gausses[:, 2]  #
        if not DrawTogether:
            # create an individual pen and brush for every gauss
            ListOfPens = []
            ListOfBrushes = []
            InsertSize = []
            for a in range(len(Gausses)):
                if Intensity[a] > LutPositions[0]:
                    #this could be changed to where-indexing, instead of append
                    XCoords.append(Gausses[a, 0])
                    YCoords.append(Gausses[a, 1])
                    InsertSize.append(Sizes[a])
                    Int = Intensity[a];
                    if Intensity[a] > LutPositions[1]:
                        Int = 1;
                    else:
                        Int = (Int - LutPositions[0]) / (LutPositions[1] - LutPositions[0])
                    Color = (
                        self.StormChannelColors[ChannelNumber][0] * Int, self.StormChannelColors[ChannelNumber][1] * Int,
                        self.StormChannelColors[ChannelNumber][2] * Int, 255 * self.StormTransparency)
                    ListOfPens.append(pg.mkPen(Color))
                    ListOfBrushes.append(pg.mkBrush(Color))
                    #display the channel
            self.DisplayedStormChannel[ChannelNumber].clear()
            pen = ListOfPens
            brush = ListOfBrushes
        else:
             ListOfPens = []
             ListOfBrushes = []
             InsertSize = []
             XCoords=Gausses[:, 0]
             YCoords=Gausses[:, 1]
             InsertSize=self.storm_dot_size # Sizes[0]
             Int = Intensity[0];
             if Intensity[0] > LutPositions[1]:
                        Int = 1;
             else:
                        Int = (Int - LutPositions[0]) / (LutPositions[1] - LutPositions[0])
             Color = (self.StormChannelColors[ChannelNumber][0] * Int, self.StormChannelColors[ChannelNumber][1] * Int,
                        self.StormChannelColors[ChannelNumber][2] * Int, 255 * self.StormTransparency)
             self.DisplayedStormChannel[ChannelNumber].clear()
             pen = pg.mkPen(Color)
             brush = pg.mkBrush(Color)

        self.DisplayedStormChannel[ChannelNumber] = self.plot_widget.plot(
            x=XCoords, y=YCoords, pen=None, symbol='o', symbolSize=InsertSize, pxMode=False, symbolPen=pen,
            symbolBrush=brush, compositionMode=pg.QtGui.QPainter.CompositionMode_Plus, opacity=self.StormTransparency)

    def ShowAllStormChannels(self):
        for ChannelNum in range(len(self.StormChannelList)):
            self.ShowStormChannel(ChannelNum)

    def ShowAllConfocalChannels(self):
        for ChannelNum in range(len(self.ConfocalMetaData)):
            self.ShowConfocalChannel(ChannelNum)

    def ShowStormChannel(self, ChannelNumber):
        if self.StormChannelVisible[ChannelNumber] and len(np.array(self.StormData_filtered[ChannelNumber]))>0:
            Gausses = np.array(self.StormData_filtered[ChannelNumber])
            LutPositions=self.StormLUTTickValues[ChannelNumber]

            if self.StormZColoring == True:
                Intensity = Gausses[:, 3]
                Intensity = Intensity - np.amin(Intensity) + 0.1
                Intensity = Intensity / np.amax(Intensity)
            else:
                Intensity = Gausses[:, 2]
                if all( Intensity==Intensity[0]) or self.main_window.groupBox_storm_config_display.isChecked():
                    DrawTogether=True
                else:
                    Intensity = 25.0 / (Gausses[:, 2]**2)

            Sizes= Gausses[:, 2]

            XCoords=Gausses[:, 0]
            YCoords=Gausses[:, 1]

            Int = Intensity[0];
            if Intensity[0] > LutPositions[1]:
                Int = 1;
            else:
                Int = (Int - LutPositions[0]) / (LutPositions[1] - LutPositions[0])

            scc = self.StormChannelColors[ChannelNumber] # 255 * self.StormTransparency
            Color = (scc[0] * Int, scc[1] * Int, scc[2] * Int, 255 * self.StormTransparency)

            self.DisplayedStormChannel[ChannelNumber] = self.plot_widget.plot(x=XCoords, y=YCoords,
                pen=None, symbolPen=None, symbol='o', symbolSize=2.5, pxMode=True,
                symbolBrush=Color, autoDownsample=True, clipToView=False)
