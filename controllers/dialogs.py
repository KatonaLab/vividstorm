# -*- coding: utf-8 -*-
"""
Created on: 2015.01.12.

Author: turbo


"""
import datetime
from functools import partial
import math

import cv2
from matplotlib import pyplot as plt
from active_contour import morphsnakes

from views.dialog_error import Ui_Dialog_error
from views.dialog_loading import Ui_Dialog_loading
from views.dialog_scale import Ui_Dialog_scale
from views.dialog_tool_active_contour import Ui_Dialog_active_contour
from views.dialog_tool_analysis import Ui_Dialog_analysis
from views.dialog_tool_lut import Ui_Dialog_lut
from views.dialog_tool_imageregistration import Ui_Dialog_imageregistration
from views.dialog_tool_positioning import Ui_Dialog_positioning
from views.dialog_view_3d import Ui_Dialog_3d
from views.dialog_view_dots import Ui_Dialog_dots
from views.dialog_view_gaussian import Ui_Dialog_gaussian
from views.dialog_about import Ui_Dialog_about
from views.dialog_help import Ui_Dialog_help_2
import numpy

import scipy
import scipy.cluster.vq as Clust

from default_config import version as version_num
from analyses import *
from scipy import ndimage
from scipy.interpolate import splprep, splev

class AboutDialog(Ui_Dialog_about):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

class HelpDialog(Ui_Dialog_help_2):
    def __init__(self, *args, **kwargs):
        super(HelpDialog, self).__init__(*args, **kwargs)

class ErrorDialog(Ui_Dialog_error):
    def __init__(self, *args, **kwargs):
        super(ErrorDialog, self).__init__(*args, **kwargs)


class LoadingDialog(Ui_Dialog_loading):
    def __init__(self, *args, **kwargs):
        super(LoadingDialog, self).__init__(*args, **kwargs)


class ScaleDialog(Ui_Dialog_scale):
    def __init__(self, *args, **kwargs):
        super(ScaleDialog, self).__init__(*args, **kwargs)

    def _setup_components(self):
        widgets = self.__dict__.keys()
        self.push_buttons = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('pushButton') != -1]

    def _add_input_handlers(self):
        for push_button in self.push_buttons:
            size = int(push_button.objectName().split('_')[-1])
            push_button.clicked.connect(partial(self.main_window.viewer.show_scale, size))

    def setup(self):
        self._setup_components()
        self._add_input_handlers()


class ActiveContourDialog(Ui_Dialog_active_contour):
    def __init__(self, *args, **kwargs):
        super(ActiveContourDialog, self).__init__(*args, **kwargs)
        self.confocal_image = None

        self.viewer = None
        self.roi = None
        self.z_position = None
        self.confocal_offset = None
        self.calibration_px = None

    def setup(self):
        self._add_input_handlers()

    def _add_input_handlers(self):
        self.pushButton_run.clicked.connect(lambda: self.run())

    def reset_channel(self):
        self.resetting = True
        while self.comboBox_confocal_channel_changer.count() > 0:
            self.comboBox_confocal_channel_changer.removeItem(0)
        self.resetting = False

    def setup_data(self, viewer, roi, z_position, confocal_offset, calibration_px):
        self.viewer = viewer
        self.roi = roi
        self.z_position = z_position
        self.confocal_offset = confocal_offset
        self.calibration_px = calibration_px

    def setup_channel(self, channel_list, channels_visible):
        comboBox = self.comboBox_confocal_channel_changer
        channels_to_add = []
        for i, channel in enumerate(channel_list):
            if channels_visible[i]:
                channels_to_add.append(str(channel))
        comboBox.addItems(channels_to_add)

    # Convert a RGB image to gray scale. (from morphsnakes)
    def Rgb2Gray(self, img):
        return 0.2989 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]

    # Build a binary function with a circle as the 0.5-levelset
    # from morphsnakes
    def ActiveContourCircleLevelset(self, shape, center, sqradius, scalerow=1.0):

        R, C = numpy.mgrid[:shape[0], :shape[1]]

        phi = sqradius - (numpy.sqrt(scalerow * (R[:, :] - center[0]) ** 2 + (C[:, :] - center[1]) ** 2))
        u = numpy.float_(phi > 0)
        return u

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

    #counts how many bordering white neighbors a black pixel has
    def CountNeighborNumber(self, x, y, matrix):
        nn = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if matrix[x + i, y + j] == 0:
                    nn += 1
        return nn

    def run(self):
        print "Active contour"

        iteration = numpy.int(self.spinBox_iteration_cycles.value())
        mu = numpy.int(self.spinBox_mu.value())
        lambda1 = numpy.int(self.spinBox_lambda1.value())
        lambda2 = numpy.int(self.spinBox_lambda2.value())
        channel = int(str(self.comboBox_confocal_channel_changer.currentText()))
        dilation_nr=numpy.int(self.spinBox_dilation.value())
        is_spline_on=self.checkBox_spline_fit.isChecked()

        """
        zpos = self.z_position

        if len(self.confocal_image.ConfocalData.shape)==2: # if 1channel, non-zstack
            img=self.confocal_image.ConfocalData/255.0 # its values should be normalized between 0 and 1
        else:
            if self.confocal_image.ConfocalMetaData['ChannelNum']>1:
                if len(self.confocal_image.ConfocalData.shape)==4:  #if non-1-channel, zstack
                    img =self.confocal_image.ConfocalData[zpos][channel] / 255.0
                else:
                    img =self.confocal_image.ConfocalData[channel] / 255.0 #if non-1-channel, non-zstack
            else:
                img =self.confocal_image.ConfocalData[zpos] / 255.0 #if 1-channel, zstack
        """
        img=self.main_window.viewer.display.ConfChannelToShow[channel]
        #downscale the image:
        
        # in case tracking active contour is needed
        #plt.figure()
        #plt.imshow(img)
        #plt.show()
        #if self.main_window.viewer.display.Viewbox.AffineTransform != []:
        #    img=cv2.warpAffine(img,self.main_window.viewer.display.Viewbox.AffineTransform,(img.shape))
        
        # Morphological ACWE. Initialization of the level-set.
        
        img=scipy.ndimage.zoom(img,  1.0/self.viewer.display.ConfocalSizeMultiplier, order=0)

        #plt.figure()
        #plt.imshow(img)
        #plt.show()

        macwe = morphsnakes.MorphACWE(img, smoothing=mu, lambda1=lambda1, lambda2=lambda2)
        zoom = 1000.0 * self.viewer.display.ConfocalMetaData['SizeX']
        
        
        conf_offset = [self.confocal_offset[0] * 100.0 * self.viewer.display.ConfocalMetaData['SizeX'],
                       self.confocal_offset[1] * 100.0 * self.viewer.display.ConfocalMetaData['SizeY']]

        position = [numpy.int((self.roi.roi.pos()[1] + self.roi.roi.size()[0] / 2.0 - conf_offset[0]) / zoom),
                    numpy.int((self.roi.roi.pos()[0] + self.roi.roi.size()[0] / 2.0 - conf_offset[1]) / zoom)]
        r = numpy.int(self.roi.roi.size()[0] / zoom / 2)

        macwe.levelset = self.ActiveContourCircleLevelset(img.shape, position, r)  #circle center coordinates, radius

        # Visual evolution.
        #plt.figure()

        acroi = morphsnakes.evolve_visual(macwe, num_iters=iteration,
                                          background=img)  # its final state is a ROI, which should be used to filter
                                          # the STORM coordinates

        # applies dilation
        if dilation_nr!=0:
            acroi = scipy.ndimage.morphology.binary_dilation(acroi, iterations=dilation_nr)

        #plt.imshow(acroi)
        #plt.figure()
        #plt.imshow(dilated_acroi)
        #plt.show()



        [edgecoords, outroi] = self.GetEdgeCoords(acroi)
        ACROI = []
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

        for i in range(len(ACROI)):
            ACROI[i] = [ACROI[i][1] * 1000.0 * self.viewer.display.ConfocalMetaData['SizeY'] + conf_offset[1] + zoom / 2.0,
                        ACROI[i][0] * 1000.0 * self.viewer.display.ConfocalMetaData['SizeX'] + conf_offset[0] + zoom / 2.0]#zoom

        if is_spline_on==True:
            # applying spline
            # spline parameters
            s = 5.0  # smoothness parameter
            k = 4  # spline order
            nest = -1  # estimate of number of knots needed (-1 = maximal)
            # find the knot points
            x = numpy.asarray(ACROI)[:, 0]

            y = numpy.asarray(ACROI)[:, 1]


            z=numpy.zeros(len(x))
            #tckp,u = scipy.interpolate.splprep([x,y,z],s=s,k=k)
            tckp,u = scipy.interpolate.splprep([x,y,z],s=s,k=k,nest=-1)

            # evaluate spline, including interpolated points
            xnew, ynew, znew = splev(numpy.linspace(0, 1, len(x) / 2), tckp)
            
            xmin=numpy.amin(x)
            xmax=numpy.amax(x)
            ymin=numpy.amin(y)
            ymax=numpy.amax(y)
            
            sxmin=numpy.amin(xnew)
            sxmax=numpy.amax(xnew)
            symin=numpy.amin(ynew)
            symax=numpy.amax(ynew)
            
            Spline=True
            if sxmin<xmin-500:
                Spline=False
            if symin<ymin-500:
                Spline=False
            if sxmax>xmax+500:
                Spline=False
            if symax>ymax+500:
                Spline=False
            # print Spline

            if Spline:
                ACROI = []
                for k in range(len(xnew)):
                    ACROI.append([xnew[k], ynew[k]])

        self.viewer.remove_roi(self.roi)
        self.viewer.add_roi('active_contour', new_roi=ACROI)
        self.formWidget.window().close()

class AnalysisDialog(Ui_Dialog_analysis):
    def __init__(self, *args, **kwargs):
        super(AnalysisDialog, self).__init__(*args, **kwargs)
        self.StormData_to_analyse = []
        self.roi_tag = None
        self.roi_perimeter = None
        self.roi_area = None

        self.analyses = []
        self.analyses.append(NlpAnalysis('analysis_nlp'))
        self.analyses.append(ConvexHullAnalysis('analysis_convex_hull'))
        self.analyses.append(DBScanAnalysis('analysis_dbscan'))
        self.analyses.append(InternalizationSurfaceAnalysis('analysis_internalization_surface'))
        self.analyses.append(InternalizationDrAnalysis('analysis_internalization_dr'))
        self.analyses.append(EuclideanDistanceWithinChannelAnalysis('analysis_euclidean_within'))
        self.analyses.append(EuclideanDistanceBetweenChannelsAnalysis('analysis_euclidean_between'))
        self.analyses.append(SurfaceDistanceBetweenChannelsAnalysis('analysis_euclidean_surface_between'))
        self.analyses.append(SurfaceDensityAnalysis('analysis_surface_density'))
        self.analyses.append(SurfaceDensityDistributionAnalysis('analysis_surface_density_distribution'))
        self.analyses.append(ExportCoordinatesTxtAnalysis('analysis_export_coords'))
        self.analyses.append(ExportCoordinatesPdbAnalysis('analysis_export_pdb'))
        self.analyses.append(QualityControlAnalysis('analysis_quality_control')) # appending new analysis
        # self.analyses.append(NewAnalysis('analysis_new')) # appending new analysis


    def setup_analyses(self, StormData_to_analyse, roi, roi_perimeter, roi_area):
        self.StormData_to_analyse = StormData_to_analyse
        if roi:
            roi_tag = str(roi.text())
        else:
            roi_tag = 'FULL_STORM_DATA'
        self.roi_tag = roi_tag
        self.roi_perimeter = roi_perimeter
        self.roi_area = roi_area
        
        for analysis in self.analyses:
            analysis.setup(self)
            analysis.setup_data(
                self.main_window.viewer.display.StormChannelList,
                self.main_window.viewer.display.StormChannelVisible,
                self.main_window.viewer.display.StormChannelColors,
                self.main_window.viewer.display.ConfocalChannelVisible,
                self.main_window.viewer.display.ConfocalChannelColors,
                self.main_window.viewer.display.ConfocalZNum,
                self.main_window.viewer.display.ConfocalData,
                self.main_window.viewer.display.ConfocalMetaData,

                roi, roi_tag, roi_perimeter, roi_area, self.main_window.viewer.display.ConfocalOffset(),
                self.checkBox_analysis_export_plots, self.groupBox_analysis_euclidean_between_confocal,
                self.main_window.viewer.display

            )
            analysis.setup_filenames(
                self.main_window.working_directory,
                self.main_window.viewer.current_storm_image.file_path,
                self.main_window.viewer.current_confocal_image
            )

    def setup(self):
        self._setup_components()
        # self._init_settings_values()
        self._add_input_handlers()

    def _setup_components(self):
        widgets = self.__dict__.keys()
        self.radio_buttons = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('radioButton') != -1]
        self.check_boxes = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('checkBox') != -1]
        self.combo_boxes = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('comboBox') != -1]
        self.spin_boxes = [getattr(self, obj_name) for obj_name in widgets if
                           (obj_name.find('spinBox') != -1 or obj_name.find('doubleSpinBox') != -1)]
        self.group_boxes = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('groupBox') != -1]


    def _add_input_handlers(self):
        for group_box in self.group_boxes:
            group_box.toggled.connect(partial(self._on_setting_changed, group_box))
        self.pushButton_analysis_run.clicked.connect(lambda: self.run_analyses())

    def setup_conf_channel(self, channel_list, channels_visible):
        comboBox = self.comboBox_analysis_euclidean_between_channel_from_confocal
        comboBox.clear()
        channels_to_add = []
        for i, channel in enumerate(channel_list):
            if channels_visible[i]:
                channels_to_add.append(str(channel))
        comboBox.addItems(channels_to_add)

    def _on_setting_changed(self, widget, is_init=False):
        setting_widget_qt_type = type(widget).__name__
        setting_key = '_'.join(str(widget.objectName()).split('_')[1:])
        if str(widget.objectName()).find('analysis') != -1:
            if setting_widget_qt_type == 'QGroupBox':
                # if this groupbox is a analysis, enable/disable the analysis
                if setting_key.find('analysis') != -1:
                    for analysis in self.analyses:
                        if analysis.name_prefix == setting_key:
                            analysis.enabled = widget.isChecked()

    def run_analyses(self):
        self.main_window.status_bar.showMessage('Running analyses, please wait...')

        values_simple = []
        for analysis in self.analyses:
            if analysis.enabled:
                StormData_to_analyse = self.StormData_to_analyse
                dimensions = '3d' if self.main_window.storm_settings.storm_config_fileheader_z else '2d'
                channels_num = len([ch for ch in self.main_window.viewer.display.StormChannelVisible if ch])
                values = analysis.run(
                    StormData_to_analyse,
                    channels_num,
                    dimensions
                )
                values_simple.append(values)
        self.write_results_common_to_file(values_simple)

        num = str(self.main_window.storm_settings.get_roi_counter())
        if type(self.analyses[0].ROI).__name__ == 'EllipseRoi':
            self.analyses[0].ROI.ChangeName("ellipseROI_"+num)
        elif type(self.analyses[0].ROI).__name__ == 'CircleRoi':
            self.analyses[0].ROI.ChangeName("circleROI_"+num)
        elif type(self.analyses[0].ROI).__name__ == 'FreehandRoi':
            self.analyses[0].ROI.ChangeName("freehandROI_"+num)   
        elif type(self.analyses[0].ROI).__name__ == 'ActiveContourRoi':
            self.analyses[0].ROI.ChangeName("activeContourROI_"+num)               
        self.main_window.storm_settings.clear_rois()
        self.main_window.storm_settings.add_roi(self.analyses[0].ROI)
       
        
        
        StormFileName=''
        if self.main_window.viewer.current_storm_image!=None:
                StormFileName=str.split(self.main_window.viewer.current_storm_image.file_path,os.sep)[-1]
        ConfocalFileName='' 
        if self.main_window.viewer.current_confocal_image!=None:  
                ConfocalFileName=str.split(self.main_window.viewer.current_confocal_image.file_path,os.sep)[-1]
        self.main_window.status_bar.showMessage('Ready '+'StormFile:'+StormFileName+' ConfocalFile:'+ConfocalFileName)
        self.scrollAreaWidgetContents.window().close()


    def write_results_common_to_file(self, computed_values_simple):
        # write to common file, simple values
        storm_file_name = os.path.basename(self.main_window.viewer.current_storm_image.file_path).split('.')[0]
        output_file_common = os.path.join(
            self.main_window.working_directory,
            storm_file_name + '_' + self.roi_tag + '_' + 'Results' + '.txt'
        )

        firstline = ''
        secondline = ''
        headers = []
        headers.append(['date_time', str(datetime.datetime.now()).split('.')[0]])
        headers.append(['version', version_num])
        headers.append(['storm_file', storm_file_name])
        headers.append(['ROI_tag', self.roi_tag])
        for header in headers:
            firstline += header[0] + '\t'
            secondline += header[1] + '\t'

        for analysis_values in computed_values_simple:
            if analysis_values:
                for value in analysis_values:
                    firstline += value[0] + '\t'
                    secondline += value[1] + '\t'
        f = open(output_file_common, 'w')
        f.write(firstline[:-1] + '\n')
        f.write(secondline[:-1]+ '\n')
        f.close()

class ImageRegistrationDialog(Ui_Dialog_imageregistration):
    def __init__(self, *args, **kwargs):
        super(ImageRegistrationDialog, self).__init__(*args, **kwargs)
        self.resetting = False

    def reset_channels(self):
        self.resetting = True
        while self.comboBox_storm_channel_changer.count() > 0:
            self.comboBox_storm_channel_changer.removeItem(0)
        while self.comboBox_confocal_channel_changer.count() > 0:
            self.comboBox_confocal_channel_changer.removeItem(0)
        self.resetting = False

    def setup_channels(self, mode, channel_list, channels_visible, RegChannelNum):
        comboBox = None
        if mode == 'storm':
            comboBox = self.comboBox_storm_channel_changer
        elif mode == 'confocal':
            comboBox = self.comboBox_confocal_channel_changer
        channels_to_add = []
        RegChannelVisible=False
        for i, channel in enumerate(channel_list):
            if channels_visible[i]:
                if i==RegChannelNum:
                    RegChannelVisible=True  
                channels_to_add.append(str(channel))
        comboBox.addItems(channels_to_add)
        if RegChannelNum!=-1 and RegChannelVisible:
            index =comboBox.findText(str(channel_list[RegChannelNum]))
            comboBox.setCurrentIndex(index)
        

    def setup(self):
        self._add_input_handlers()

    def _add_input_handlers(self):
        self.comboBox_storm_channel_changer.currentIndexChanged.connect(
            lambda: self.change_channel('storm', self.comboBox_storm_channel_changer.currentText()))
        self.comboBox_confocal_channel_changer.currentIndexChanged.connect(
            lambda: self.change_channel('confocal', self.comboBox_confocal_channel_changer.currentText()))
        self.pushButton_manual_selection.clicked.connect(lambda: self.put_manual_markers())
        self.pushButton_delete_markers.clicked.connect(lambda: self.delete_markers())
        self.pushButton_Registration.clicked.connect(lambda: self.Register())
        self.pushButton_automatic_selection.clicked.connect(lambda: self.AutomaticMarkers())

    def AutomaticMarkers(self): 
        self.delete_markers()
        Scale=1000.0/self.main_window.viewer.display.ConfocalSizeMultiplier
        ScaleX=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']
        ScaleY=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeY']
        #add storm markers
        #k-means on Storm point
        G=numpy.array(self.main_window.viewer.display.StormData_filtered[self.main_window.viewer.display.Viewbox.StormRegistrationChannel])
        #SelectedCentroids,tmp=Clust.kmeans(G[:,0:2],3)
        #Select the three most dense regions instead of k-means:
        AllStormPoints=G[:,0:2]
        SelectedCentroids=[[AllStormPoints[0,0],AllStormPoints[0,1]], [AllStormPoints[1,0],AllStormPoints[1,1]], [AllStormPoints[2,0] , AllStormPoints[2,1]]]
        Neighbours=[0, 0, 0]
        Radius=200
        PointNum=0
        for StP in AllStormPoints:
            PointNum+=1
            Neighbourpoints=0
            SumCentroid=[0, 0]
            DistanceMatrix=numpy.sqrt(numpy.square(AllStormPoints[:,0]-StP[0])+numpy.square(AllStormPoints[:,1]-StP[1]))
            Candidates=numpy.where(DistanceMatrix<Radius)
            Neighbourpoints=len(Candidates[0])
            NewCentroid=numpy.mean(AllStormPoints[Candidates],0)
            
            ind=0
            NotInserted=True
            while ind<len(Neighbours) and NotInserted:
                #this is a new maximum, instert it
                if Neighbours[ind]<Neighbourpoints:
                    #check if the current point is not inserted:
                    NotClose=True
                    for a in SelectedCentroids:
                        if math.sqrt(math.pow(a[0]-NewCentroid[0],2)+math.pow(a[1]-NewCentroid[1],2))<Radius:
                            NotClose=False
                    if NotClose:    
                        Neighbours[ind]=Neighbourpoints
                        NotInserted=False
                        SelectedCentroids[ind][0]=NewCentroid[0]
                        SelectedCentroids[ind][1]=NewCentroid[1]
                ind+=1
        for c in SelectedCentroids:
            Marker= pg.ROI([0, 0])
            self.main_window.viewer.display.Viewbox.StormMarkerRois.append(Marker)
            Marker.addTranslateHandle([c[0],c[1]],[0.5, 0.5])   
            Handle=Marker.getHandles()[0]                  
            Handle.sides=4
            Handle.startAng=0
            Handle.buildPath()
            Handle.generateShape()                             
            self.main_window.viewer.display.plot_widget.addItem(Marker)
            #add confocal markers for storm marker
            
            Image=numpy.asarray(self.main_window.viewer.display.DisplayedConfocalChannel[self.main_window.viewer.display.Viewbox.ConfRegistrationChannel].image)
            
            MidX=int(c[1]/ScaleX)
            MidY=int(c[0]/ScaleY)
            #searhc for appropriate point in 5 % of the image distance
            radius=int(Image.shape[0]*0.05)
            FromX=max(MidX-radius,0)
            TillX=min(MidX+radius,Image.shape[0])
            FromY=max(MidY-radius,0)
            TillY=min(MidY+radius,Image.shape[1])
            Cut=Image[FromX:TillX,FromY:TillY]
            Max=numpy.argmax(Cut)
            Xorig=(Max/Cut.shape[0])
            Yorig=(Max-(Xorig*Cut.shape[0]))
            Y=int(ScaleX*(Xorig+MidX-Cut.shape[0]/2))
            X=int(ScaleY*(Yorig+MidY-Cut.shape[1]/2))
            Marker= pg.ROI([0, 0])
            self.main_window.viewer.display.Viewbox.ConfMarkerRois.append(Marker)
            #shift the points based on the confocal shift position
            X+=self.main_window.viewer.display.Viewbox.ConfocalOffset[1]*ScaleX
            Y+=self.main_window.viewer.display.Viewbox.ConfocalOffset[0]*ScaleY
            Marker.addFreeHandle([X,Y])                    
            self.main_window.viewer.display.plot_widget.addItem(Marker)
       

        
    def Register(self): 
        #check if we have enough markers
        if self.main_window.viewer.display.Viewbox.AffineTransform != []:
            self.main_window.show_error(message='Images are alredy registered, please reload Confocal data for new registration') 
        elif len(self.main_window.viewer.display.Viewbox.StormMarkerRois)!=3 and len(self.main_window.viewer.display.Viewbox.ConfMarkerRois)!=3:
            self.main_window.show_error(message='Not enough marker points for registration')            
        else:
            Aff=numpy.zeros((2,3))
            StormPoints=numpy.ones((3,3))
            ConfocalPoints=numpy.ones((3,3))
            Scale=1000.0/self.main_window.viewer.display.ConfocalSizeMultiplier
            ScaleX=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']
            ScaleY=Scale * self.main_window.viewer.display.ConfocalMetaData['SizeY']
            Index=0
            for roi in self.main_window.viewer.display.Viewbox.ConfMarkerRois:
                P=roi.getLocalHandlePositions()[0][1]
                ConfocalPoints[Index,0]=((P.x()-self.main_window.viewer.display.Viewbox.ConfocalOffset[0])/float(ScaleX))
                ConfocalPoints[Index,1]=((P.y()-self.main_window.viewer.display.Viewbox.ConfocalOffset[1])/float(ScaleY))
                Index+=1
            Index=0
            for roi in self.main_window.viewer.display.Viewbox.StormMarkerRois:
                P=roi.getLocalHandlePositions()[0][1]
                StormPoints[Index,0]=(P.x()/float(ScaleX))
                StormPoints[Index,1]=(P.y()/float(ScaleY))
                Index+=1
            # Pad the data with ones, so that our transformation can do translations too
            n = ConfocalPoints.shape[0]
            X = numpy.matrix(ConfocalPoints)
            Y = numpy.matrix(StormPoints)
            # Solve the least squares problem X * Aff = Y
            # to find our transformation matrix Aff
            A=X.I*Y
            
            ConfShape=self.main_window.viewer.display.ConfChannelToShow.shape
            Aff[:2,:2]=A[:2,:2]
            tmp=Aff[1,0]
            Aff[1,0]=Aff[0,1]
            Aff[0,1]=tmp
            Aff[0,2]=A[2,0]
            Aff[1,2]=A[2,1]
            self.main_window.viewer.display.Viewbox.AffineTransform = Aff
            #apply affine transformation
            for ChInd in range(ConfShape[0]):
                self.main_window.viewer.display.ConfChannelToShow[ChInd,:,:]=cv2.warpAffine(self.main_window.viewer.display.ConfChannelToShow[ChInd,:,:],Aff,(self.main_window.viewer.display.ConfChannelToShow[ChInd,:,:].shape))
            #adjust confocal markers to strom markers
            for RoiInd in range(len(self.main_window.viewer.display.Viewbox.ConfMarkerRois)):
                Marker= pg.ROI([0, 0])
                OldPoints=self.main_window.viewer.display.Viewbox.StormMarkerRois[RoiInd].getLocalHandlePositions()[0][1]
                self.main_window.viewer.display.plot_widget.removeItem(self.main_window.viewer.display.Viewbox.ConfMarkerRois[RoiInd]) 
                self.main_window.viewer.display.Viewbox.ConfMarkerRois[RoiInd]=Marker
                Marker.addFreeHandle([OldPoints.x(),OldPoints.y()])
                self.main_window.viewer.display.plot_widget.addItem(Marker) 
            self.main_window.viewer.display.ShowAll()
            
    def put_manual_markers(self):
        self.main_window.show_error(message=u'Place three storm (◇) and three confocal Markers (□)')
        self.main_window.viewer.display.Viewbox.ClickMode='Reg'

    def delete_markers(self):  
        self.main_window.viewer.display.Viewbox.ClickMode='Norm'      
        for Roi in self.main_window.viewer.display.Viewbox.StormMarkerRois:
            self.main_window.viewer.display.plot_widget.removeItem(Roi)                 
        for Roi in self.main_window.viewer.display.Viewbox.ConfMarkerRois:
            self.main_window.viewer.display.plot_widget.removeItem(Roi)
        self.main_window.viewer.display.Viewbox.StormMarkerRois=[]
        self.main_window.viewer.display.Viewbox.ConfMarkerRois=[]
            
    def change_channel(self, mode, channel_name):
        if channel_name and not self.resetting:
            channel_num =  None
            if mode == 'storm':
                channel_num = self.main_window.viewer.display.StormChannelList.index(channel_name)
                self.main_window.viewer.display.Viewbox.SetRegistrationChannelStorm(channel_num)
            elif mode == 'confocal':
                channel_num = range(self.main_window.viewer.display.ConfocalMetaData['ChannelNum']).index(
                    int(str(channel_name)))
                self.main_window.viewer.display.Viewbox.SetRegistrationChannelConf(channel_num)
                
class LutDialog(Ui_Dialog_lut):
    def __init__(self, *args, **kwargs):
        super(LutDialog, self).__init__(*args, **kwargs)
        self.resetting = False

    def reset_channels(self):
        self.resetting = True
        while self.comboBox_storm_channel_changer.count() > 0:
            self.comboBox_storm_channel_changer.removeItem(0)
        while self.comboBox_confocal_channel_changer.count() > 0:
            self.comboBox_confocal_channel_changer.removeItem(0)
        self.resetting = False

    def setup_channels(self, mode, channel_list, channels_visible):
        comboBox = None
        if mode == 'storm':
            comboBox = self.comboBox_storm_channel_changer
        elif mode == 'confocal':
            comboBox = self.comboBox_confocal_channel_changer
        channels_to_add = []
        for i, channel in enumerate(channel_list):
            if channels_visible[i]:
                channels_to_add.append(str(channel))
        comboBox.addItems(channels_to_add)

    def setup(self):
        self._add_input_handlers()

    def _add_input_handlers(self):
        self.comboBox_storm_channel_changer.currentIndexChanged.connect(
            lambda: self.change_channel('storm', self.comboBox_storm_channel_changer.currentText()))
        self.comboBox_confocal_channel_changer.currentIndexChanged.connect(
            lambda: self.change_channel('confocal', self.comboBox_confocal_channel_changer.currentText()))

    def change_channel(self, mode, channel_name):
        if channel_name and not self.resetting:
            channel_num = channel_color = None
            if mode == 'storm':
                channel_num = self.main_window.viewer.display.StormChannelList.index(channel_name)
                channel_color = self.main_window.viewer.display.StormChannelColors[channel_num]
                self.main_window.viewer.display.ShowStormLut(channel_num, channel_color)
            elif mode == 'confocal':
                channel_num = range(self.main_window.viewer.display.ConfocalMetaData['ChannelNum']).index(
                    int(str(channel_name)))
                channel_color = self.main_window.viewer.display.ConfocalChannelColors[channel_num]
                self.main_window.viewer.display.ShowConfocalLut(channel_num, channel_color)


class PositioningDialog(Ui_Dialog_positioning):
    def __init__(self, *args, **kwargs):
        super(PositioningDialog, self).__init__(*args, **kwargs)


class ThreeDDialog(Ui_Dialog_3d):
    def __init__(self, *args, **kwargs):
        super(ThreeDDialog, self).__init__(*args, **kwargs)


class DotsDialog(Ui_Dialog_dots):
    def __init__(self, *args, **kwargs):
        super(DotsDialog, self).__init__(*args, **kwargs)


class GaussianDialog(Ui_Dialog_gaussian):
    def __init__(self, *args, **kwargs):
        super(GaussianDialog, self).__init__(*args, **kwargs)
