__author__ = 'Judit'

import scipy
import math
import numpy
from sklearn.metrics.pairwise import pairwise_distances
import igraph
import matplotlib.pyplot as plt
import matplotlib

def minus(self,v,xlim):
    return v-[xlim[1]-xlim[0], 0]

def plus(self,v,xlim):
    return v+[xlim[1]-xlim[0],0]

def minus2(self,v,ylim):
    return v - [0, ylim[1]-ylim[0]]

def plus2(self,v,ylim):
    return v + [0, ylim[1]-ylim[0]]

def plus3(self,v,xlim,ylim):
    return v + [xlim[1]-xlim[0], -(ylim[1]-ylim[0])]

def plus4(self,v,xlim,ylim):
    return v + [-(xlim[1]-xlim[0]), -(ylim[1]-ylim[0])]

def plus5(self,v,xlim,ylim):
    return v + [-(xlim[1]-xlim[0]), ylim[1]-ylim[0]]

def plus6(self,v,xlim,ylim):
    return v + [xlim[1]-xlim[0], ylim[1]-ylim[0]]

def toroid(self,pts, xlim, ylim, range):


    R = pts[pts[: ,0] >= (xlim[1]-range), :]
    Rshift=numpy.array([self.minus(p, xlim) for p in R])
    L=pts[pts[:, 0] <= (xlim[0]+range), :]
    Lshift=numpy.array([self.plus(p, xlim) for p in L])
    U = pts[pts[:, 1] >= (ylim[1]-range), :]
    Ushift = numpy.array([self.minus2(p, ylim) for p in U])
    D=pts[pts[:, 1] <= (ylim[0]+range), :]
    Dshift=numpy.array([self.plus2(p, ylim) for p in D])

    LU=pts[(pts[:, 0] <= (xlim[0]+range)) & (pts[:, 1] >= (ylim[1]-range)), :]
    LUshift=numpy.array([self.plus3(p, xlim,ylim) for p in LU])
    RU=pts[(pts[:, 0] >= (xlim[1]-range)) & (pts[:, 1] >= (ylim[1]-range)), :]
    RUshift=numpy.array([self.plus4(p, xlim,ylim) for p in RU])
    RD=pts[(pts[:, 0] >= (xlim[1]-range)) & (pts[:,1] <= (ylim[0]+range)), :]
    RDshift=numpy.array([self.plus5(p, xlim,ylim) for p in RD])
    LD=pts[(pts[:, 0] <= (xlim[0]+range)) & (pts[:, 1] <= (ylim[0]+range)), :]
    LDshift=numpy.array([self.plus6(p, xlim,ylim) for p in LD])
    if len(Rshift>0):
        pts=numpy.concatenate((pts,Rshift))
    if len(Lshift>0):
        pts=numpy.concatenate((pts,Lshift))
    if len(Ushift>0):
         pts=numpy.concatenate((pts,Ushift))
    if len(Dshift>0):
        pts=numpy.concatenate((pts,Dshift))
    if len(LUshift>0):
        pts=numpy.concatenate((pts,LUshift))
    if len(RUshift>0):
        pts=numpy.concatenate((pts,RUshift))
    if len(RDshift>0):
        pts=numpy.concatenate((pts,RDshift))
    if len(LDshift>0):
        pts=numpy.concatenate((pts,LDshift))
    return pts

def mcgaussprec(self, pts, sds, xlim=range(0, 1), ylim=range(0, 1), psd=0, minsd=0.1, maxsd=100, grid=100):

    N = pts.shape[0]
    def divide(p):
        return 1/p
    def fsd1(sd):
        x = math.pow(sd, 2)
        y = numpy.power(sds, 2)
        def f(y):
            return x+y
        a = map(f, y)
        wts = map(divide, a)
        tilden = sum(wts)
        mu = numpy.array([sum(numpy.multiply(wts, pts[:, 0]))/tilden, sum(numpy.multiply(wts, pts[:, 1]))/tilden])

        c = numpy.array([numpy.multiply(wts, numpy.power(numpy.add(pts[:, 0], - mu[0]), 2)), numpy.multiply(wts, \
                                                                        numpy.power(numpy.add(pts[:, 1], -mu[1]), 2))])
        totdist = sum(sum(c))

        tm = math.log(scipy.stats.norm.cdf(math.sqrt(tilden)*(xlim[1]-mu[0])) - \
                    scipy.stats.norm.cdf(math.sqrt(tilden)*(xlim[0] - mu[0]))) + \
                    math.log(scipy.stats.norm.cdf(math.sqrt(tilden)*(ylim[1]-mu[1])) - \
                    scipy.stats.norm.cdf(math.sqrt(tilden)*(ylim[0] - mu[1]))) - \
                    (N-1)*math.log(2*math.pi)+sum(numpy.log(wts))- \
                    totdist/2-math.log((xlim[1]-xlim[0])*(ylim[1]-ylim[0]))-math.log(tilden)
        a = tm + psd(self,sd)

        return a
    x = numpy.linspace(minsd, maxsd, num=grid)
    x = x[1:len(x)-1]
    x = numpy.append(x, maxsd)

    values = map(fsd1, x)
    dx = x[1]-x[0]
    m = numpy.amax(values)

    def f2(x):
        return x-m
    int = sum(numpy.exp(map(f2, values)))*dx

    b = math.log(int)+m
    return b

def plabel(self,labels, alpha, pb,points):

        ar = []
        cl = []
        for i in labels:
            exsist = False
            a = len(ar)
            for j in range(0, a):
                if i == ar[j]:
                    exsist = True
            if exsist == False:
                ar.append(i)
        tmp = numpy.array(range(0, len(points)))

        for i in ar:
            t = numpy.where(labels == i)[0]
            t2 = tmp[t]
            if len(t2) > 1:
                new = len(t2)
                cl.append(new)

        B = len(labels)-sum(cl)

        Bcont = B*math.log(pb)+(1-B)*math.log(1-pb)
        partcont = 0
        if len(cl) > 0:

            def funcgamma(v):
                return math.lgamma(v)
            partcont3 = sum(map(funcgamma, cl))
            partcont = len(cl)*math.log(alpha)+math.lgamma(alpha)-math.lgamma(alpha+sum(cl))+partcont3
        return Bcont+partcont

def scorewprec(self, labels, pts, sd, xlim, ylim, psd, minsd, maxsd, useplabel=True, alpha=0, pb=0.5):

    def func1(v):
        if len(v) > 1:
            sds = numpy.array(sd)
            a = self.mcgaussprec(pts[v, :], sds[v], xlim, ylim, psd, minsd, maxsd)
        else:
            a = -math.log((xlim[1]-xlim[0])*(ylim[1]-ylim[0]))
        return a

    values = []
    z = 0
    ar = []
    for i in labels:
        exsist = False
        a = len(ar)
        for j in range(0, a):
            if i == ar[j]:
                exsist = True
        if exsist == False:
                ar.append(i)
    tmp = numpy.array(range(0, len(pts)))
    for i in ar:
        t = numpy.where(labels == i)[0]
        t2 = tmp[t]
        new = func1(t2)
        values.append(new)
        z = z+new
    s = sum(values)
    prlab = 0
    if useplabel:
        if alpha == 0:
            alpha = 20
        prlab = self.plabel(labels, alpha, pb,pts)
    return s+prlab

def Kclust(self,pts, xlim, ylim, rseq, thseq,sds=0, psd=0, minsd=0, maxsd=0, useplabel=True, alpha=0, pb=0.5, \
               score=True, rlabel=False, report=True,hv=[]):
        """
        print pts
        print pts.shape
        print xlim
        print ylim
        print rseq
        print thseq
        print sds
        print minsd
        print maxsd
        print alpha
        print pb
        exit(0)
        """
        svector=[]
        results = []
        pts0=pts
        pts=pts[:,0:2]
        N = pts.shape[0]
        tor = self.toroid(pts, xlim, ylim, max(rseq))
        D = pairwise_distances(tor)
        D = D[0:N, 0:N]

        for r in rseq:
            rvector=[]
            zline = []

            def func1(v):
                return (sum(v <= r)-1)
            K = map(func1, D)

            def func2(v):
                return ((xlim[1]-xlim[0]+2*max(rseq))*(ylim[1]-ylim[0]+2*max(rseq))*v)/(math.pi*(len(tor)-1))
            L = numpy.sqrt(map(func2, K))

            rvector1 = []
            rvector2 = []
            clustered2 = False
            for th in thseq:
                clustered=False
                C = numpy.where(L >= th)[0]


                A = pts[:, 0][C]
                B = pts[:, 1][C]
                Z = pts0[:, 2][C]


                C2 = numpy.array(C)

                if len(C2) > 0:
                    clustered = True
                    clustered2 = True
                    Q = D[numpy.ix_(C2, C2)]

                    def func4(v):
                        return (v < (2*r))
                    W = map(func4, Q)
                    WW = numpy.asarray(W)
                    W3 = numpy.matrix(WW)
                    G = igraph.Graph.Adjacency(W3.tolist())
                    lab = G.clusters(mode='weak')
                    lab2 = lab.membership
                    labels = numpy.array(range(N, (2*N)))
                    labels[C2] = lab2

                else:
                    labels = numpy.array(range(0, N))
                if score:
                    ex = False
                    for i in range(len(results)):
                        equal=True
                        if (len(labels) != len(results[i][0])):
                            equal=False
                        else:
                            for j in range(len(labels)):
                                if (labels[j]!=results[i][0][j]):
                                    equal=False
                                    break
                        if equal:
                            s=results[i][1]
                            ex=True

                    if ex==False:
                        s = self.scorewprec(labels, pts, sds, xlim, ylim, psd, minsd, maxsd, useplabel, \
                                                alpha, pb)
                        results.append([labels, s])

                    rvector1.append(s)

                    if clustered:
                        cl_index=[0]*len(pts)
                        for i in range(len(C)):
                            cl_index[C[i]] = lab.membership[i]+1


                        rvector2.append(len(lab))

                        svector.append([r, th, s, lab, A, B, cl_index,Z,C])


                    else:
                        svector.append([r,th,s,0,A,B,C])
                        rvector2.append(0)




            index=0

            for i in range(len(rvector1)):
                if rvector1[i] < rvector1[index]:
                    index = i

            if clustered2:
                hv.append(rvector2[index])
            else:
                hv.append(0)
        return svector

"""
def compute(self, points):
    print 'Bayesian_clustering_analysis'

    channel_nr = numpy.where(numpy.asarray(self.storm_channels_visible) == True)
    visible_channel_nr = numpy.asarray(channel_nr)[0]

    for m in visible_channel_nr:
        if len(points[m]) > 0:
            coords = numpy.empty((len(points[m]), 2), dtype=numpy.int)
            sdvalues = numpy.empty((len(points[m]), 1), dtype=numpy.float)
            coords[:, 0] = numpy.asarray(points[m])[:, 0]
            coords[:, 1] = numpy.asarray(points[m])[:, 1]
            sdvalues = numpy.asarray(points[m])[:, 2]
        pbackground=self.analysis_bayesian_pbackground
        rseq=numpy.arange(self.analysis_bayesian_rseqmin,self.analysis_bayesian_rseqmax+1, \
                              self.analysis_bayesian_rseqdiff)
        thseq=numpy.arange(self.analysis_bayesian_thseqmin,self.analysis_bayesian_thseqmax+1, \
                               self.analysis_bayesian_thseqdiff)
        alpha=self.analysis_bayesian_alpha
        if self.analysis_bayesian_usehistogram:
            pass
        else:
            histbins = [10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, \
                            350, 370, 390, 410, 430, 450, 470, 490, 510, 530, 550, 570, 590]
            histvalues = [8, 57, 104, 130, 155, 168, 197, 205, 216, 175, 123, 91, 74, 32, 24, 22, 12, 11, \
                              6, 5, 3, 5, 1, 3, 0, 4, 0, 1, 1, 1]

        xlim=[]
        ylim=[]

        if self.ROI:
            xcoords=[]
            ycoords=[]
            if (type(self.ROI).__name__ == 'CircleRoi') | (type(self.ROI).__name__ == 'EllipseRoi'):
                roi = self.ROI.roi.mapToParent(self.ROI.roi.shape())
                element_nr = roi.elementCount()
                for k in range(element_nr):
                    xcoords.append(roi.elementAt(k).x)
                    ycoords.append(roi.elementAt(k).y)
            elif type(self.ROI).__name__ == 'FreehandRoi':
                roi=self.ROI.roi.shape()
                element_nr=roi.elementCount()
                for k in range(element_nr):
                    xcoords.append(roi.elementAt(k).x)
                    ycoords.append(roi.elementAt(k).y)
            elif type(self.ROI).__name__ == 'ActiveContourRoi':
                PolygonItem = self.ROI.roi[0]
                roi=PolygonItem.shape()
                element_nr=roi.elementCount()
                for k in range(element_nr):
                    xcoords.append(roi.elementAt(k).x)
                    ycoords.append(roi.elementAt(k).y)
            xlim=numpy.array([min(xcoords),max(xcoords)])
            ylim=numpy.array([min(ycoords),max(ycoords)])
        else:
            xlim = numpy.array([min(coords[:, 0]), max(coords[:, 0])])
            ylim = numpy.array([min(coords[:, 1]), max(coords[:, 1])])

        minsd = histbins[0]
        maxsd = histbins[len(histbins)-1]
        useplabel=True
        f = scipy.interpolate.interp1d(histbins, histvalues)
        cst = scipy.integrate.quad(f, histbins[0], histbins[len(histbins)-1])[0]
        def psd(self,sd):
            if (f(sd)==0):
                return (math.log(0.0001)-math.log(cst))
            else:
                return (math.log(f(sd))-math.log(cst))
        hv=[]

        svector=self.Kclust(pts=coords, xlim=xlim, ylim=ylim, rseq=numpy.arange(10, 591, 20), thseq=thseq, sds=sdvalues, psd=psd, minsd=minsd, \
                        maxsd=maxsd, useplabel=useplabel, alpha=alpha, pb=pbackground, hv=hv)

        histvalues = hv
        f = scipy.interpolate.interp1d(histbins, histvalues)
        cst = scipy.integrate.quad(f, histbins[0], histbins[len(histbins)-1])[0]

        svector=self.Kclust(pts= coords, xlim=xlim, ylim=ylim, rseq=rseq, thseq=thseq, sds=sdvalues, psd=psd, minsd=minsd, maxsd=maxsd, \
                        useplabel=useplabel, alpha=alpha, pb=pbackground,hv=hv)

        maxv = svector[0][2]

        ind = 0
        for i in range(len(svector)):
            if svector[i][2] > maxv:
                maxv = svector[i][2]
                ind = i

        ok=True
        try:
            print (svector[ind][3].membership)
        except:
            ok=False

            print ("Not clustered")

        if ok:
            r=svector[ind][0]
            th=svector[ind][1]
            A=svector[ind][4]
            B=svector[ind][5]

            counter=[]
            memberships=[]

            rs=[]
            ths=[]
            ss=[]
            memberships.append(svector[ind][3].membership)
            As=[]
            As.append(svector[ind][4])
            all=[]
            all.append([svector[ind][2],svector[ind][3],svector[ind][4],svector[ind][5]])
            rs.append(svector[ind][0])
            ths.append(svector[ind][1])
            ss.append(svector[ind][2])
            counter.append(1);
            for i in range(len(svector)):
                if svector[ind][2] == svector[i][2]:
                    exist=False
                    for j in range(len(memberships)):
                        if svector[i][3]!=0:
                            if numpy.array_equal(memberships[j],svector[i][3].membership) & numpy.array_equal(As[j],svector[i][4]):
                                exist=True
                                counter[j]=counter[j]+1
                    if exist==False:
                        if (svector[i][3]!=0):
                            memberships.append(svector[i][3].membership)
                            As.append(svector[i][4])
                            rs.append(svector[i][0])
                            ths.append(svector[i][1])
                            ss.append(svector[i][2])
                            all.append([svector[i][2],svector[i][3],svector[i][4],svector[i][5]])
                            counter.append(1)

            maxind=[]
            for i in range(len(counter)):
                if (counter[i]==max(counter)):
                    maxind.append(i)

            maxind=maxind[0]
            for i in range(len(svector)):
                if (svector[i][3]!=0):
                    if (memberships[maxind]==svector[i][3].membership):
                        ind=i
                        break

            A=svector[ind][4]
            B=svector[ind][5]
            list=svector[ind][3]
            ivector=[]
            for i in list:
                if (len(i)==1):
                    for j in i:
                        ivector.append(j)

            ivector2=[]
            avector=[]
            bvector=[]
            for j in range(len(ivector)):
                ivector2.append(svector[ind][3].membership[ivector[j]])
                avector.append(ivector[j])


            clust_number = len(svector[ind][3])

            vec=svector[ind][3].membership
            clustnums=set(vec)
            #svector[ind][3].membership=np.array([svector[ind][3].membership])
            for i in range(len(ivector2)):
                vec.remove(ivector2[i])
                clust_number=clust_number-1
                clustnums.remove(ivector2[i])
            A = numpy.delete(A, avector)
            B = numpy.delete(B, avector)

            if self.display_plots == True:

                colorlist = numpy.ones((len(vec), 3))

                for s in range(clust_number):
                    inds = numpy.where(numpy.asarray(vec) == s + 1)
                    assignedcolor = matplotlib.colors.hsv_to_rgb([(s / 1.0) / clust_number, 1.0, 1.0])
                    colorlist[inds, :] = numpy.asarray(assignedcolor)

                fig=plt.figure(facecolor=(0, 0, 0), edgecolor=(0, 0, 0))
                fig.hold(True)
                fig.patch.set_facecolor((0, 0, 0))
                ax1=fig.add_subplot(111, axisbg='k', projection='3d', aspect='equal')
                ax1.grid(False)
                ax1.set_axis_off()
                ax1.set_frame_on(False)
                ax1.set_title('Bayesian clustering', color='w')
                ax1.scatter(A, B, c=numpy.asarray(colorlist), marker='o')
                ax1.set_xlabel('x coordinates [nm]',fontsize=15)
                ax1.set_ylabel('y coordinates [nm]',fontsize=15)
                plt.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=14)
                plt.setp(ax1.get_yticklabels(), fontsize=14)
                plt.gca().invert_yaxis()
                plt.gca().set_aspect('equal')
                plt.show()

            print "Bayesian_clustering_analysis ready"
"""