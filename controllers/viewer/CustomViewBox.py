import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from .. import default_config
import numpy

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.StromDisplay=None
        self.ChannelNum=0
        self.ScaleBar = []
        self.ScaleSize = 0
        self.ScaleText = ''
        self.Window = []
        self.FreehandRoi = []
        self.DrawnRoi = []
        self.StormRegistrationChannel = -1
        self.ConfRegistrationChannel = -1
        self.DrawnRoi = []
        self.ConfocalOffset = [0, 0]
        self.StormMarkerRois = []
        self.ConfMarkerRois = []
        self.PanMode = default_config.viewer_input_mode
        self.ClickMode ='Norm'
        self.AffineTransform = []

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):        
        if self.ClickMode == 'Reg':
            Current = self.mapToView(ev.pos())
            Marker= pg.ROI([0, 0])
            if len(self.StormMarkerRois)<3:
                self.StormMarkerRois.append(Marker)
                Marker.addFreeHandle([Current.x(),Current.y()])
                Handle=Marker.getHandles()[0]                  
                Handle.sides=4
                Handle.startAng=0
                Handle.buildPath()
                Handle.generateShape()
                self.StormDisplay.plot_widget.addItem(Marker)
            else:
                if len(self.ConfMarkerRois)<3:
                    self.ConfMarkerRois.append(Marker)
                    Marker.addFreeHandle([Current.x(),Current.y()])
                    self.StormDisplay.plot_widget.addItem(Marker) 
                else:  
                    self.ClickMode='Norm'  
                          
        else:
            pg.ViewBox.mouseClickEvent(self, ev)

    def SetRegistrationChannelStorm(self,StormChannelNum):
        self.StormRegistrationChannel=StormChannelNum
        
    def SetRegistrationChannelConf(self,ConfChannelNum):
        self.ConfRegistrationChannel=ConfChannelNum
         
    def mouseDragEvent(self, ev):
        if self.PanMode == 'Pan':
            pg.ViewBox.mouseDragEvent(self, ev)
        elif self.PanMode == 'Conf':
            cursorOffset = ev.screenPos() - ev.lastScreenPos()
            # scale to pixel coordinates
            XTrans = cursorOffset[0] * self.viewPixelSize()[0] / 8
            YTrans = cursorOffset[1] * self.viewPixelSize()[1] / 8
            self.ConfocalOffset = [self.ConfocalOffset[0] + YTrans, self.ConfocalOffset[1] + XTrans]
            
            for CN in range(4):
                if self.StormDisplay.DisplayedConfocalChannel[CN] != 0:
                    self.StormDisplay.DisplayedConfocalChannel[CN].translate(YTrans, XTrans)
            #move the registration markers if there are any:
            Scale=1000.0/self.StormDisplay.ConfocalSizeMultiplier
            for RoiInd in range(len(self.main_window.viewer.display.Viewbox.ConfMarkerRois)):
                Marker= pg.ROI([0, 0])
                OldPoints=self.ConfMarkerRois[RoiInd].getLocalHandlePositions()[0][1]
                self.StormDisplay.plot_widget.removeItem(self.ConfMarkerRois[RoiInd]) 
                self.ConfMarkerRois[RoiInd]=Marker
                Marker.addFreeHandle([OldPoints.x()+XTrans*Scale * self.StormDisplay.ConfocalMetaData['SizeX'],OldPoints.y()+YTrans*Scale * self.StormDisplay.ConfocalMetaData['SizeY']])
                self.StormDisplay.plot_widget.addItem(Marker) 
            #calcualte correlation between confocal and storm channel
            
            #if event is finished display registration correlation
            if ev.isFinish():
                #if the displayed channels exist:
                if self.ConfRegistrationChannel!=-1 and self.StormRegistrationChannel!=-1:
                    #if the channels are displayed:
                    if self.StormDisplay.DisplayedConfocalChannel[self.ConfRegistrationChannel]!=0 and self.StormDisplay.DisplayedStormChannel[self.StormRegistrationChannel]!=0:
                        #maybe rescale the images if really slow;Or precalculate an image and just index from it
                        Im1=self.StormDisplay.DisplayedConfocalChannel[self.ConfRegistrationChannel]
                        Im2=self.StormDisplay.DisplayedStormChannel[self.StormRegistrationChannel]
                        
                        Scale=1000.0/self.StormDisplay.ConfocalSizeMultiplier
                        Correlation=0
                        for ind in range(len(Im2.getData()[0])):
                            IndX=(int(Im2.getData()[0][ind])/(Scale * self.StormDisplay.ConfocalMetaData['SizeX']))-self.ConfocalOffset[1]
                            IndY=(int(Im2.getData()[1][ind])/(Scale * self.StormDisplay.ConfocalMetaData['SizeY']))-self.ConfocalOffset[0]
                            if IndX>-1 and IndX<Im1.image.shape[1] and IndY>-1 and IndY<Im1.image.shape[0]:
                                Correlation+=Im1.image[IndY,IndX]
                        Msg=self.main_window.status_bar.currentMessage()
                        Msg=str.split(str(Msg),' Correlation:')[0]
                        #find a possible norm of correlation
                        #mean might be a more representative value for normalization:numpy.mean(Im1.image)
                        MaxCorr=len(Im2.getData()[0])*Im1.image.max()
                        self.main_window.status_bar.showMessage(Msg+' Correlation: '+ str(float(Correlation)/float(MaxCorr)) )
                else:
                    Msg=self.main_window.status_bar.currentMessage()
                    Msg=str.split(str(Msg),' Correlation:')[0]
                    self.main_window.status_bar.showMessage(Msg+' Correlation: The selected channels are not displayed' )
            #print signal.correlate2d(Im1,Im2)
            if self.main_window.viewer.display.ConfocalSizeMultiplier==1:
                Scale=1000*self.main_window.viewer.display.ConfocalSizeMultiplier
            else:
                Scale=10*self.main_window.viewer.display.ConfocalSizeMultiplier
            self.main_window.doubleSpinBox_confocal_display_offset_x.setValue(
                int(self.ConfocalOffset[1] * Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']))
            self.main_window.doubleSpinBox_confocal_display_offset_y.setValue(
                int(self.ConfocalOffset[0] * Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']))
            ev.accept()
            pos = ev.pos()

            modifiers = QtGui.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier and ev.button() == QtCore.Qt.LeftButton:
                if ev.isFinish():
                    # self.traj_widget.update_selection_infos()
                    self.rbScaleBox.hide()
                else:
                    rect_box = QtCore.QRectF(pg.Point(ev.buttonDownPos(ev.button())), pg.Point(pos))
                    rect_box = self.childGroup.mapRectFromParent(rect_box)
                    self.update_selection(rect_box)
                    self.traj_widget.update_selection_infos()
                    self.updateScaleBox(ev.buttonDownPos(), ev.pos())
        elif self.PanMode == 'Roi':
            Current = self.mapToView(ev.pos())
            Prev = self.mapToView(ev.lastPos())
            r1 = pg.QtGui.QGraphicsLineItem(Prev.x(), Prev.y(), Current.x(), Current.y())
            r1.setPen(pg.mkPen('w'))
            self.DrawnRoi.append(r1)
            self.addItem(r1)
            self.FreehandRoi.append(Current)
            # closing curve on finish
            if ev.isFinish():
                Current = self.mapToView(ev.buttonDownPos())
                Prev = self.mapToView(ev.pos())
                r1 = pg.QtGui.QGraphicsLineItem(Prev.x(), Prev.y(), Current.x(), Current.y())
                r1.setPen(pg.mkPen('w'))
                self.DrawnRoi.append(r1)
                self.addItem(r1)
                self.FreehandRoi.append(Current)

            ev.accept()
            pos = ev.pos()
            modifiers = QtGui.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier and ev.button() == QtCore.Qt.LeftButton:
                if ev.isFinish():
                    # self.traj_widget.update_selection_infos()
                    self.rbScaleBox.hide()
                else:
                    rect_box = QtCore.QRectF(pg.Point(ev.buttonDownPos(ev.button())), pg.Point(pos))
                    rect_box = self.childGroup.mapRectFromParent(rect_box)
                    self.update_selection(rect_box)
                    self.traj_widget.update_selection_infos()
                    self.updateScaleBox(ev.buttonDownPos(), ev.pos())

    def deleteFreehandROI(self, roi):
        for r in self.DrawnRoi:
            self.removeItem(r)
        self.FreehandRoi = []
        self.DrawnRoi = []
        roi = None
 
 
    def deleteActiveContourROI(self, DrawnElements):
        for r in DrawnElements:
            self.removeItem(r)

    def deleteEllipseROI(self, roi):
        self.removeItem(roi)

    def updateMatrix(self, changed=None):
        # keep scale bar at same position
        if self.ScaleBar != []:
            ViewRange = self.viewRange()
            XLength = (ViewRange[0][1] - ViewRange[0][0]) * 0.05
            YLength = (ViewRange[1][1] - ViewRange[1][0]) * 0.05
            Xpos = ViewRange[0][0] + XLength
            Ypos = ViewRange[1][0] + YLength
            self.ScaleBar.clear()
            self.Window.removeItem(self.ScaleText)
            self.ScaleBar = self.Window.plot(x=[Xpos, Xpos + self.ScaleSize], y=[Ypos, Ypos], symbol='o')
            PosX = Xpos
            PosY = Ypos + YLength * 0.1
            self.ScaleText = pg.TextItem(text=str(self.ScaleSize) + ' nm', color=(200, 200, 200))
            self.Window.addItem(self.ScaleText)
            self.ScaleText.setPos(PosX, PosY)
        pg.ViewBox.updateMatrix(self, changed=None)


    def setScaleBar(self, ScaleBar, Window, Size, Text):
        self.ScaleBar = ScaleBar
        self.Window = Window
        self.ScaleSize = Size
        self.ScaleText = Text

    def deleteScaleBar(self):
        if self.ScaleBar != []:
            self.ScaleBar.clear()
            self.Window.removeItem(self.ScaleText)
            self.ScaleBar = []
            self.ScaleSize = 0
            self.ScaleText = ''

    def setWindow(self, Window):
        self.Window = Window

    def deleteConfocalImage(self):
        self.StromDisplay = None

    def setConfocalImage(self, StormDisplay, ChannelNum):
        self.StormDisplay = StormDisplay
        self.ChannelNum = ChannelNum

