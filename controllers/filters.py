# -*- coding: utf-8 -*-
"""
Created on: 2015.01.11.

Author: turbo


"""

import numpy
import scipy
from scipy import spatial
from numpy import *

from util import RunnableComponent


class Filter(RunnableComponent):
    def __init__(self, *args, **kwargs):
        super(Filter, self).__init__(*args, **kwargs)

    def run(self, points):
        return points


#deletes localizations that are outside the given z range
class ZFilter(Filter):
    def __init__(self, *args, **kwargs):
        super(ZFilter, self).__init__(*args, **kwargs)

    def run(self, points):
        print "ZFilter"
        out=[]

        for k in range(len(points)):

            indsplus=numpy.where(numpy.asarray(points[k])[:,3]>self.storm_filter_z_to)
            indsminus=numpy.where(numpy.asarray(points[k])[:,3]<self.storm_filter_z_from)
            inds2=numpy.union1d(indsplus[0],indsminus[0])

            if list(numpy.delete(numpy.asarray(points[k]),inds2,0))==[]:
                out.append(numpy.asarray([]))
            else:
                out.append(list(numpy.delete(numpy.asarray(points[k]),inds2,0)))

        return out

class PhotonFilter(Filter):
    def __init__(self, *args, **kwargs):
        super(PhotonFilter, self).__init__(*args, **kwargs)

    def run(self, points):
        print 'PhotonFilter'
        out=[]
        for k in range(len(points)):
            indsplus=numpy.where(numpy.asarray(points[k])[:,4]>self.storm_filter_photon_to)

            indsminus=numpy.where(numpy.asarray(points[k])[:,4]<self.storm_filter_photon_from)
            inds2=numpy.union1d(indsplus[0],indsminus[0])
            if list(numpy.delete(numpy.asarray(points[k]),inds2,0))==[]:
                out.append(numpy.asarray([]))
            else:
                out.append(list(numpy.delete(numpy.asarray(points[k]),inds2,0)))
        return out

class FrameFilter(Filter):
    def __init__(self, *args, **kwargs):
        super(FrameFilter, self).__init__(*args, **kwargs)

    def run(self, points):
        print 'FrameFilter'
        outpoints=[]
        for k in range(len(points)):
            indsplus=numpy.where(numpy.asarray(points[k])[:,6]>self.storm_filter_frame_to)

            indsminus=numpy.where(numpy.asarray(points[k])[:,6]<self.storm_filter_frame_from)
            inds2=numpy.union1d(indsplus[0],indsminus[0])
            if list(numpy.delete(numpy.asarray(points[k]),inds2,0))==[]:
                outpoints.append(numpy.asarray([]))
            else:
                outpoints.append(list(numpy.delete(numpy.asarray(points[k]),inds2,0)))

        return outpoints

class LocalDensityFilter(Filter):
    def __init__(self, *args, **kwargs):
        super(LocalDensityFilter, self).__init__(*args, **kwargs)

    def run(self, points):
        """filter data for localizations with n neighbors within eps.
        Returns list of indices of included points."""
        print "LdFilter"
        outpoints=[]
        for k in range(len(points)):
            rsd=numpy.empty((len(points[k]), 3), dtype=numpy.int)
            rsd[:,0]=numpy.asarray(points[k])[:,0]
            rsd[:,1]=numpy.asarray(points[k])[:,1]
            rsd[:,2]=numpy.asarray(points[k])[:,3]
            filt=[]
            tree=scipy.spatial.cKDTree(rsd)
            for i in range(len(rsd)):
                if (len(tree.query_ball_point(rsd[i], self.storm_filter_localdensity_maxradius))-1)<self.storm_filter_localdensity_min_num:
                    filt.append(i)
            if list(numpy.delete(numpy.asarray(points[k]),filt,0))==[]:
                outpoints.append(numpy.asarray([]))
            else:
                outpoints.append(list(numpy.delete(numpy.asarray(points[k]),filt,0)))
        return outpoints

class InternalizationFilter(Filter):
     def __init__(self, *args, **kwargs):
         super(InternalizationFilter, self).__init__(*args, **kwargs)

