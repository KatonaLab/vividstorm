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

from default_config import version as \
    version_num
from analyses import *
from scipy import ndimage
from scipy.interpolate import splprep, splev
import images
import settings
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtCore import QString
import matplotlib.pyplot as plt

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
        self.StormData_to_analyse = None

    def setup(self):
        self._add_input_handlers()

    def _add_input_handlers(self):
        self.pushButton_run.clicked.connect(lambda: self.run())

    def reset_channel(self):
        self.resetting = True
        while self.comboBox_confocal_channel_changer.count() > 0:
            self.comboBox_confocal_channel_changer.removeItem(0)
        self.resetting = False

    def setup_data(self, viewer, roi, z_position, confocal_offset, calibration_px,StormData_to_analyse):
        self.viewer = viewer
        self.roi = roi
        self.z_position = z_position
        self.confocal_offset = confocal_offset
        self.calibration_px = calibration_px
        self.StormData_to_analyse = StormData_to_analyse

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
                try:
                    if matrix[x + i, y + j] == 0:
                        nn += 1
                except:
                    nn +=1
        return nn

    def CountNeighborNumber_3d(self, z, y, x, matrix):


            nn = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    for k in range(-1,2):

                        if matrix[z+k , y + i,x+j] == 0:
                            nn += 1
            return nn

    def GetEdgeCoords_3d(self, matrix):
        start_plane=0
        end_plane=0
        actual_last_slice=0
        for x in range(numpy.shape(matrix)[0]):
            for y in range(numpy.shape(matrix)[1]):
                for z in range(numpy.shape(matrix)[2]):
                    if matrix[x, y,z] == 1:
                        if start_plane==0:
                            start_plane=x
                        actual_last_slice=x
        end_plane=actual_last_slice


        edgecoords = []
        outmatrix = numpy.copy(matrix)

        for x in range(numpy.shape(matrix)[0]):
            for y in range(numpy.shape(matrix)[1]):
                for z in range(numpy.shape(matrix)[2]):
                    if matrix[x, y,z] == 1:
                        if x != start_plane and x!=end_plane:
                            nn = self.CountNeighborNumber_3d(x, y,z, matrix)
                        else:
                            nn = 1
                        if nn > 0:

                            edgecoords.append([x, y,z])

        return edgecoords

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
        zoom =1000.0 * self.viewer.display.ConfocalMetaData['SizeX']
        for i in range(len(ACROI)):
            ACROI[i] = [ACROI[i][1] * 1000.0 * self.viewer.display.ConfocalMetaData['SizeY'] + self.confocal_offset[1] * 100.0 * self.viewer.display.ConfocalMetaData['SizeY'] + zoom / 2.0,
                        ACROI[i][0] * 1000.0 * self.viewer.display.ConfocalMetaData['SizeX'] + self.confocal_offset[0] * 100.0 * self.viewer.display.ConfocalMetaData['SizeX'] + zoom / 2.0]#zoom
        return ACROI


    def matrix_order_wo_conv(self,xy_roi_full):
            xy_roi_edge = []
            CurrentPoint = xy_roi_full[0]
            xy_roi_edge.append(CurrentPoint)
            PointAdded = True
            while PointAdded:
                PointAdded=False
                NeighbouringPoints=0
                MinDist=2
                MinPoint=[]
                for point in xy_roi_full:
                    if math.fabs(CurrentPoint[0]-point[0])<2 and math.fabs(CurrentPoint[1]-point[1])<2:
                        Dist=math.sqrt((CurrentPoint[0]-point[0])*(CurrentPoint[0]-point[0])+(CurrentPoint[1]-point[1])
                                       *(CurrentPoint[1]-point[1]))
                        if Dist<MinDist and Dist!=0:
                            MinDist=Dist
                            MinPoint=point
                if MinPoint!=[]:
                    PointAdded=True
                    xy_roi_full.remove(MinPoint)
                    xy_roi_edge.append(MinPoint)
                    CurrentPoint=MinPoint
            return xy_roi_edge


    def run(self):
        print "Active contour"

        iteration = numpy.int(self.spinBox_iteration_cycles.value())
        mu = numpy.int(self.spinBox_mu.value())
        lambda1 = numpy.int(self.spinBox_lambda1.value())
        lambda2 = numpy.int(self.spinBox_lambda2.value())
        channel = int(str(self.comboBox_confocal_channel_changer.currentText()))
        dilation_nr=numpy.int(self.spinBox_dilation.value())
        is_spline_on=self.checkBox_spline_fit.isChecked()
        dim_2 = self.radioButton_2D.isChecked()

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
        numpy.set_printoptions(threshold=numpy.nan)
        if not dim_2:

            channel_storm = self.main_window.viewer.display.StormChannelVisible.index(True)
            subarray = []
            numpy.set_printoptions(threshold=numpy.nan)
            #print self.confocal_image.ConfocalData[0][0][0].dtype
            if len(self.main_window.viewer.display.ConfChannelToShow) == 1:
                subarray = self.confocal_image.ConfocalData
            else:
                for i in range(len(self.confocal_image.ConfocalData)):
                    subarray.append(self.confocal_image.ConfocalData[len(self.confocal_image.ConfocalData)-i-1][channel])

            img = numpy.array(subarray)
            self.formWidget.window().close()

            macwe = morphsnakes.MorphACWE(img, smoothing=mu, lambda1=lambda1, lambda2=lambda2)
            macwe.levelset = morphsnakes.circle_levelset(img.shape, (self.z_position,position[0],position[1]), r)
            acroi=morphsnakes.evolve_visual3d(macwe, num_iters=iteration)
            if dilation_nr > 0:
                acroi = scipy.ndimage.morphology.binary_dilation(acroi, iterations=dilation_nr)

            [edgecoords_z_pos, outroi] = self.GetEdgeCoords(acroi[self.z_position])
            ACROI = self.matrix_order(edgecoords_z_pos)

            edgecoords_3d = self.GetEdgeCoords_3d(acroi)

            inside_pixels=[]
            for i in range(len(acroi)):
                for j in range(len(acroi[0])):
                    for k in range(len(acroi[0][0])):
                        if acroi[i][j][k]==1:
                            inside_pixels.append([i, j, k])

            for i in range(len(edgecoords_3d)):
                inside_pixels.remove(edgecoords_3d[i])


            for i in range(len(inside_pixels)):
                inside_pixels[i] =(inside_pixels[i][2] * 1000.0 * self.viewer.display.ConfocalMetaData['SizeX'] + conf_offset[1]+self.viewer.display.ConfocalMetaData['SizeX']/2,
                                       inside_pixels[i][1] * 1000.0 * self.viewer.display.ConfocalMetaData['SizeY'] + conf_offset[0]+self.viewer.display.ConfocalMetaData['SizeY']/2,
                                          inside_pixels[i][0] * 1000.0 * self.viewer.display.ConfocalMetaData['SizeZ']-1050)

            from math import sqrt,pow
            sx=self.viewer.display.ConfocalMetaData['SizeX']*1000/2
            sy=self.viewer.display.ConfocalMetaData['SizeY']*1000/2
            sz=self.viewer.display.ConfocalMetaData['SizeZ']*1000/2
            atlo= sqrt(pow(sx,2)+pow(sy*2,2))
            mind=sqrt(pow(atlo,2)+pow(sz*2,2))
            mind=sqrt(pow(sx*2,2)+pow(sz*2,2))

            from scipy.spatial import distance
            inside_roi=[]

            for i in range(len(self.StormData_to_analyse[channel_storm])):
                #self.StormData_to_analyse[channel_storm][i][3] = self.StormData_to_analyse[channel_storm][i][3]
                for j in range(len(inside_pixels)):

                    if distance.euclidean(numpy.array([self.StormData_to_analyse[channel_storm][i][0],self.StormData_to_analyse[channel_storm][i][1],self.StormData_to_analyse[channel_storm][i][3]]),inside_pixels[j]) <= mind:
                        inside_roi.append(numpy.array(self.StormData_to_analyse[channel_storm][i]))
                        break
            inside_roi_storm = numpy.array(inside_roi)

            #storm->konfokális
            xm=position[1]-r-5
            ym=position[0]-r-5

            for i in range(len(inside_roi)):
                x1 = int((float(inside_roi[i][0]-conf_offset[1])/self.viewer.display.ConfocalMetaData['SizeX']/1000-xm)*5)
                y1 = int((float(inside_roi[i][1]-conf_offset[0])/self.viewer.display.ConfocalMetaData['SizeY']/1000-ym)*5)
                z1 = int((float(inside_roi[i][3]+150*self.z_position+self.viewer.display.ConfocalMetaData['SizeZ']*1000/2)/self.viewer.display.ConfocalMetaData['SizeZ']/1000)*10)
                inside_roi[i]=numpy.array([x1,y1,z1])

            subarray2=[]
            for i in range(len(img)):
                sub1=[]
                for j in range(position[0]-r-5,position[0]+r+5,1):
                    sub2=[]
                    for k in range(position[1]-r-5,position[1]+r+5,1):
                        sub2.append(img[i][j][k])
                    sub1.append(sub2)
                subarray2.append(sub1)
            subarray2=numpy.array(subarray2)

            max_pr_xy = numpy.amax(subarray2, axis=0)
            max_pr_xz = numpy.amax(subarray2, axis=1)
            max_pr_yz = numpy.amax(subarray2, axis=2).transpose()


            [xy_roi_full, outroi] = self.GetEdgeCoords(numpy.amax(acroi, axis=0))
            xy_roi_edge = self.matrix_order_wo_conv(xy_roi_full)

            pg1=[]
            for i in range(len(xy_roi_edge)):
                a= xy_roi_edge[i][0] - (position[0]-r-5)
                b= xy_roi_edge[i][1] - (position[1]-r-5)
                pg1.append((5*b+2,5*a+2))
            pg1.append((pg1[0]))

            #xz plane
            [xz_roi_full, outroi] = self.GetEdgeCoords(numpy.amax(acroi, axis=1))
            xz_roi_edge = self.matrix_order_wo_conv(xz_roi_full)

            pg2=[]
            for i in range(len(xz_roi_edge)):
                b = xz_roi_edge[i][1] - (position[1]-r-5)
                pg2.append((b, xz_roi_edge[i][0]))
            pg2.append((pg2[0]))

            #yz plane
            max_roi_yz = numpy.amax(acroi, axis=2)
            [yz_roi_full, outroi] = self.GetEdgeCoords(max_roi_yz)
            yz_roi_edge = self.matrix_order_wo_conv(yz_roi_full)

            pg3=[]
            for i in range(len(yz_roi_edge)):
                b= yz_roi_edge[i][1] - (position[0]-r-5)
                pg3.append(( yz_roi_edge[i][0],b))
            pg3.append((pg3[0]))

            #RGB
            xy=numpy.zeros((len(max_pr_xy),len(max_pr_xy[0]),3), dtype=numpy.uint8)
            for i in range(len(max_pr_xy)):
                for j in range(len(max_pr_xy[0])):
                    xy[i,j,1]=max_pr_xy[i][j]


            from PIL import ImageDraw
            import PIL.Image

            slicesview=numpy.zeros((5*len(max_pr_xy[0])+5*len(max_pr_xz)*2,5*len(max_pr_xy)+2*5*len(max_pr_yz[0]),3),dtype=numpy.uint8)
            slicesview[:,:,:]+=255

            im=PIL.Image.fromarray(slicesview,'RGB')
            im1=PIL.Image.fromarray(xy,'RGB').resize((5*len(xy),5*len(xy)),resample=PIL.Image.NEAREST)
            from shapely.geometry import Polygon,Point
            draw1=ImageDraw.Draw(im1)
            poly1=Polygon(pg1)
            for i in range(len(inside_roi)):
                if poly1.contains(Point(inside_roi[i][0], inside_roi[i][1])):
                    im1.putpixel((inside_roi[i][0], inside_roi[i][1]),(255,0,0))
            draw1.line(pg1,width=2)
            im.paste(im1,box=(0,0))
            a=numpy.zeros((len(max_pr_xz),len(max_pr_xz[0]),3), dtype=numpy.uint8)
            for i in range(len(max_pr_xz)):
                for j in range(len(max_pr_xz[0])):
                    a[i,j,1]=max_pr_xz[i][j]
            b=numpy.zeros((len(max_pr_yz),len(max_pr_yz[0]),3), dtype=numpy.uint8)
            for i in range(len(max_pr_yz)):
                for j in range(len(max_pr_yz[0])):
                    b[i,j,1]=max_pr_yz[i][j]
            im2 = PIL.Image.fromarray(a,'RGB').resize((5*len(max_pr_xz[0]),5*2*len(max_pr_xz)),resample=PIL.Image.NEAREST)
            draw2=ImageDraw.Draw(im2)
            for i in range(len(pg2)):
                pg2[i]=(5*pg2[i][0]+2, 5*2*pg2[i][1]+4)
            pg2.append(pg2[0])
            poly2=Polygon(pg2)
            for i in range(len(inside_roi)):
                if poly2.contains(Point(inside_roi[i][0], inside_roi[i][2])):
                    im2.putpixel((inside_roi[i][0],inside_roi[i][2]),(255,0,0))
            draw2.line(pg2,width=2)
            im.paste(im2,box=(0,5*len(max_pr_xy)))
            im3 = PIL.Image.fromarray(b,'RGB').resize((5*2*len(max_pr_yz[0]),5*len(max_pr_yz)),resample=PIL.Image.NEAREST)
            draw3=ImageDraw.Draw(im3)

            for i in range(len(pg3)):
                pg3[i]=(5*2*pg3[i][0]+4,5*pg3[i][1]+2)
            pg3.append(pg3[0])
            poly3=Polygon(pg3)


            for i in range(len(inside_roi)):
                if poly3.contains(Point(inside_roi[i][2], inside_roi[i][1])):
                    im3.putpixel((inside_roi[i][2],inside_roi[i][1]),(255,0,0))

            draw3.line(pg3,width=2)
            im.paste(im3,box=(5*len(max_pr_xy),0))
            plt.imshow(im,interpolation="nearest")
            plt.axis("off")
            plt.show()
            self.viewer.remove_roi(self.roi)
            inside_roi3=[]
            for i in range(4):
                inside_roi3.append([])
            inside_roi3[channel_storm] = inside_roi_storm
            self.viewer.add_roi_3d(new_roi=acroi, xy_pointlist=ACROI, storm_inside=inside_roi3)

        else:

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
        self.main = None
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
        self.analyses.append(QualityControlAnalysis('analysis_quality_control'))
        self.analyses.append(BayesianClusteringAnalysis('analysis_bayesian'))
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
        self.line_edits = [getattr(self, obj_name) for obj_name in widgets if obj_name.find('lineEdit') != -1]

    def choose_histogram_file(self):

        if self.checkBox_analysis_bayesian_usehistogram.isChecked():
            file_dialog = QtGui.QFileDialog()
            title = "Choose histogram file"
            extension = "histogram file (*.txt)"
            file_hist = QtGui.QFileDialog.getOpenFileName(file_dialog, title,
                                                            "/home", extension)
            self.lineEdit_analysis_bayesian_histogramlinedit.setText(file_hist)

    def choose_batch_analyses_folder(self):

        if self.radioButton_analysis_batch.isChecked():
            folder_dialog = QtGui.QFileDialog()
            folder_dialog.setFileMode(QtGui.QFileDialog.Directory)
            folder_dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
            title = "Choose folder"
            batch_folder_name = QtGui.QFileDialog.getExistingDirectory(folder_dialog,title, self.main_window.working_directory)
            self.lineEdit_analysis_folder_name.setText(batch_folder_name)

    def choose_batch_analyses_roiattr(self):
        if self.radioButton_analysis_batch.isChecked():
            folder_dialog = QtGui.QFileDialog()
            folder_dialog.setFileMode(QtGui.QFileDialog.Directory)
            folder_dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
            title = "Choose folder"
            batch_folder_name = QtGui.QFileDialog.getExistingDirectory(folder_dialog,title, self.main_window.working_directory)

            self.lineEdit_analysis_roiattr_name.setText(batch_folder_name)

    def choose_batch_analyses_roicoords(self):
        if self.radioButton_analysis_batch.isChecked():
            folder_dialog = QtGui.QFileDialog()
            folder_dialog.setFileMode(QtGui.QFileDialog.Directory)
            folder_dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
            title = "Choose folder"
            batch_folder_name = QtGui.QFileDialog.getExistingDirectory(folder_dialog,title,self.main_window.working_directory)

            self.lineEdit_analysis_roicoords_name.setText(batch_folder_name)

    def choose_batch_analyses_confocal(self):
        if self.radioButton_analysis_batch.isChecked():
            folder_dialog = QtGui.QFileDialog()
            folder_dialog.setFileMode(QtGui.QFileDialog.Directory)
            folder_dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
            title = "Choose folder"
            batch_folder_name = QtGui.QFileDialog.getExistingDirectory(folder_dialog,title, self.main_window.working_directory)

            self.lineEdit_analysis_confocal_name.setText(batch_folder_name)


    def _add_input_handlers(self):
        for group_box in self.group_boxes:
            group_box.toggled.connect(partial(self._on_setting_changed, group_box))
        self.pushButton_analysis_run.clicked.connect(lambda: self.run_analyses())
        self.pushButton_analysis_bayesian_choose_file.clicked.connect(lambda: self.choose_histogram_file())
        self.pushButton_analysis_batch_choose_folder.clicked.connect(lambda: self.choose_batch_analyses_folder())
        self.pushButton_analysis_batch_choose_roiattr.clicked.connect(lambda: self.choose_batch_analyses_roiattr())
        self.pushButton_analysis_batch_choose_roicoords.clicked.connect(lambda: self.choose_batch_analyses_roicoords())
        self.pushButton_analysis_batch_choose_confocal.clicked.connect(lambda: self.choose_batch_analyses_confocal())

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

    def run_batch_analyses(self):
        print "Batch analyses"


        roicoords_folder = self.lineEdit_analysis_roicoords_name.text()
        result_folder = self.lineEdit_analysis_folder_name.text()

        roiattr_folder = self.lineEdit_analysis_roiattr_name.text()

        confocal_folder = self.lineEdit_analysis_confocal_name.text()

        if roiattr_folder == "":
            roiattr_folder = roicoords_folder
        if result_folder == "":
            result_folder = roicoords_folder
        if confocal_folder == "":
            confocal_folder = roicoords_folder



        self.main_window.status_bar.showMessage('Running analyses, please wait...')

        result_files = os.listdir(result_folder)
        result_files2=[]
        for file in result_files:
            if file.endswith('_Results.txt'):
                result_files2.append(file)

        roicoords_files = os.listdir(roicoords_folder)
        roicoords_files2=[]
        for file in roicoords_files:
            if file.endswith('.txt') and not file.endswith('_RoiAttr.txt') and not file.endswith('_Results.txt'):
                roicoords_files2.append(file)

        roiattr_files = os.listdir(roiattr_folder)
        roiattr_files2=[]
        for file in roiattr_files:
            if file.endswith('_RoiAttr.txt'):
                roiattr_files2.append(file)
        confocal_files = os.listdir(confocal_folder)
        confocal_files2=[]
        for file in confocal_files:
            if file.endswith('.tif'):
                confocal_files2.append(file)

        conf_b=False
        roi_b=False
        res_b=False

        if len(confocal_files2) > 0:
             conf_b = True
        if len(roiattr_files2) > 0:
            roi_b= True
        if len(result_files2) > 0:
            res_b=True

        if self.main_window.viewer.current_confocal_image is not None and conf_b:

            tmp = self.main_window.viewer.current_confocal_image
            tmp2 = self.main_window.viewer.display.ConfocalData
            tmp3 = self.main_window.viewer.display.ConfocalMetaData
            tmp4 = self.main_window.viewer.display.ConfocalOffset()
            tmp5 = self.main_window.viewer.display.ConfChannelToShow
            a = str(tmp4[0])
            b = str(tmp4[1])

        if roi_b:
            for file in roicoords_files2:
                print file
                tag=file[:file.find('.txt')]
                tag2=file[:file.find('_RoiCoords.txt')]
                filepath_w = file
                storm_image = images.StormImage(file)
                storm_image.coords_cols = (self.main_window.storm_settings.storm_config_fileheader_x,\
                                           self.main_window.storm_settings.storm_config_fileheader_y,\
                                           self.main_window.storm_settings.storm_config_fileheader_z)
                storm_image.other_cols = (
                    self.main_window.storm_settings.storm_config_fileheader_localization_precision,
                    self.main_window.storm_settings.storm_config_fileheader_channel_name,
                    self.main_window.storm_settings.storm_config_fileheader_photon,
                    self.main_window.storm_settings.storm_config_fileheader_frame
                )
                storm_image.file_path = roicoords_folder+'/'+tag+'.txt'
                storm_image.parse()
                roi_border= []

                with open(roiattr_folder+'/'+tag2+'_RoiAttr.txt') as attr_file:

                        line = attr_file.readline()
                        line = attr_file.readline()

                        y_offset, x_offset = [float(x) for x in line.split()]
                        for i in range(0, 2):
                            line = attr_file.readline()
                        roi_tag = line[:-1]
                        line = attr_file.readline()
                        """
                        if roi_tag == "FreehandROI":
                            index = str(storm_image.file_path).find("freehandROI")
                            index2 = str(storm_image.file_path).find("RoiCoords")-1
                            roi_tag = str(storm_image.file_path)[index:index2]
                        elif roi_tag == "CircleROI":
                            index = str(storm_image.file_path).find("circleROI")
                            index2 = str(storm_image.file_path).find("RoiCoords")-1
                            roi_tag = str(storm_image.file_path)[index:index2]
                        elif roi_tag == "EllipseROI":
                            index = str(storm_image.file_path).find("ellipseROI")
                            index2 = str(storm_image.file_path).find("RoiCoords")-1
                            roi_tag = str(storm_image.file_path)[index:index2]
                        """
                        if line == "ROI confocal pixel number\n":
                            for i in range(0, 4):
                                line = attr_file.readline()

                            conf_name = attr_file.readline()


                            line = attr_file.readline().split()

                            while line:
                                line = attr_file.readline().split()
                                if line:
                                    roi_border.append(line)
                attr_file.close()

                conf_name=None
                x_offset=None
                y_offset=None
                if conf_name is not None and self.main_window.viewer.current_confocal_image is not None and conf_b:

                    confocal_image = images.ConfocalImage(QString(str(conf_name)))
                    confocal_image.file_path = str(confocal_folder + '/' + conf_name[:-1])
                    confocal_image_name = str(confocal_folder + '/' + conf_name[:-1])

                    confocal_image.parse(self.main_window.confocal_settings.confocal_config_calibration_px, self.main_window)
                    #self.main_window.viewer.display.Viewbox = [y_offset, x_offset]
                    self.main_window.viewer.current_confocal_image = confocal_image
                    self.main_window.viewer.display.ConfocalData = confocal_image.ConfocalData
                    self.main_window.viewer.display.ConfocalMetaData = confocal_image.ConfocalMetaData
                    Scale=1000*self.main_window.viewer.display.ConfocalSizeMultiplier

                    self.main_window.doubleSpinBox_confocal_display_offset_x.setValue(
                    int(x_offset * Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']))
                    self.main_window.doubleSpinBox_confocal_display_offset_y.setValue(
                    int(y_offset * Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']))
                    px = self.main_window.viewer.display.ConfocalMetaData['SizeX']

                    self.main_window.viewer.display.Viewbox.ConfocalOffset = [
                    self.main_window.confocal_settings.confocal_display_offset_y / (100 * px),
                    self.main_window.confocal_settings.confocal_display_offset_x / (100 * px)

                    ]

                else:
                    confocal_image_name = ""






                values_simple = []
                StormData_to_analyse = storm_image.StormData
                dimensions = '3d' if self.main_window.storm_settings.storm_config_fileheader_z else '2d'
                channels_num = len([ch for ch in self.main_window.viewer.display.StormChannelVisible if ch])
                StormData_to_analyse = self.main_window.storm_settings.filter_storm_data(StormData_to_analyse)

                for analysis in self.analyses:
                    if analysis.enabled:
                        if not confocal_image_name == "":
                            values = analysis.run_batch(
                                StormData_to_analyse,
                                channels_num,
                                dimensions,
                                filepath_w,
                                roi_tag,
                                confocal_image_name,
                                [y_offset, x_offset],
                                confocal_image,
                                confocal_image.ConfocalMetaData,

                            )
                        else:
                            values = analysis.run_batch(
                                StormData_to_analyse,
                                channels_num,
                                dimensions,
                                filepath_w,
                                roi_tag,
                                "",
                                [y_offset, x_offset],
                                "",
                                "",

                            )
                        values_simple.append(values)

                self.write_results_common_to_file_batch(values_simple, file[:-14])
        else:
            #print 'original STORM file analysis'
            for file in roicoords_files2:
                print file
                tag=file[:file.find('.txt')]
                filepath_w = file

                storm_image = images.StormImage(file)
                storm_image.coords_cols = (self.main_window.storm_settings.storm_config_fileheader_x,\
                                               self.main_window.storm_settings.storm_config_fileheader_y,\
                                               self.main_window.storm_settings.storm_config_fileheader_z)
                storm_image.other_cols = (
                        self.main_window.storm_settings.storm_config_fileheader_localization_precision,
                        self.main_window.storm_settings.storm_config_fileheader_channel_name,
                        self.main_window.storm_settings.storm_config_fileheader_photon,
                        self.main_window.storm_settings.storm_config_fileheader_frame
                )
                storm_image.file_path = roicoords_folder+'/'+tag+'.txt'
                storm_image.parse()
                if "freehandROI" in file:
                    roi_tag= 'freehandROI'
                elif "circleROI" in file:
                    roi_tag= 'circleROI'
                elif "ellipseROI" in file:
                    roi_tag= 'ellipseROI'
                elif "activeContourROI" in file:
                    roi_tag= 'activeContourROI'
                else:
                    roi_tag= 'FULL STORM DATA'
                values_simple = []
                StormData_to_analyse = storm_image.StormData
                dimensions = '3d' if self.main_window.storm_settings.storm_config_fileheader_z else '2d'
                channels_num = len([ch for ch in self.main_window.viewer.display.StormChannelVisible if ch])
                StormData_to_analyse = self.main_window.storm_settings.filter_storm_data(StormData_to_analyse)

                for analysis in self.analyses:
                    if analysis.enabled:
                        values = analysis.run_batch(
                                StormData_to_analyse,
                                channels_num,
                                dimensions,
                                filepath_w,
                                roi_tag,
                                "",
                                "",
                                "",
                                "",
                        )
                        values_simple.append(values)
                if "RoiCoords" in file:
                    self.write_results_common_to_file_batch(values_simple, file[:-14])
                else:
                    self.write_results_common_to_file_batch(values_simple, file[:-4])

        if self.main_window.viewer.current_confocal_image is not None and conf_b:
            tmp.parse(self.main_window.confocal_settings.confocal_config_calibration_px, self.main_window)
            self.main_window.viewer.current_confocal_image = tmp
            self.main_window.viewer.display.ConfocalData = tmp2
            self.main_window.viewer.display.ConfocalMetaData = tmp3
            Scale=1000*self.main_window.viewer.display.ConfocalSizeMultiplier

            self.main_window.doubleSpinBox_confocal_display_offset_x.setValue(
                int(x_offset * Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']))
            self.main_window.doubleSpinBox_confocal_display_offset_y.setValue(
                int(y_offset * Scale * self.main_window.viewer.display.ConfocalMetaData['SizeX']))
            px = self.main_window.viewer.display.ConfocalMetaData['SizeX']

            self.main_window.viewer.display.Viewbox.ConfocalOffset = [
                    float(a),
                    float(b)

                    ]
            self.main_window.viewer.display.ConfChannelToShow = tmp5
        values_simple = []
        StormData_to_analyse = storm_image.StormData
        StormData_to_analyse = self.main_window.storm_settings.filter_storm_data(StormData_to_analyse)
        print "Batch analysis ready"

    def run_analyses(self):
        if self.radioButton_analysis_single.isChecked():
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
        elif self.lineEdit_analysis_roicoords_name.text() == "":

            self.main_window.show_error(message='No STORM file folder is chosen!')
        else:
            self.run_batch_analyses()
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

    def write_results_common_to_file_batch(self, computed_values_simple, filename):
        #filepath = self.lineEdit_analysis_roicoords_name.text()+'/results/'+filename+ '_Results.txt'
        filepath = self.main_window.working_directory+'/'+filename+ '_Results.txt'

        firstline = ''
        secondline = ''
        headers = []
        headers.append(['date_time', str(datetime.datetime.now()).split('.')[0]])
        headers.append(['version', version_num])
        headers.append(['storm_file', filename])
        #headers.append(['ROI_tag', self.roi_tag])
        for header in headers:
            firstline += header[0] + '\t'
            secondline += header[1] + '\t'

        for analysis_values in computed_values_simple:
            if analysis_values:
                for value in analysis_values:
                    firstline += value[0] + '\t'
                    secondline += value[1] + '\t'
        f = open(filepath, 'w')
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
