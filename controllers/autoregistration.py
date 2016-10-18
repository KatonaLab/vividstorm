import numpy as np
import scipy
import scipy.signal
from pyqtgraph.Qt import QtGui
import pyqtgraph.exporters
from PyQt4.QtGui import *
import cv2


GlobalDownscale=10.0

def cross_image(im1_gray, im2_gray):
   # get rid of the color channels by performing a grayscale transform
   # the type cast into 'float' is to avoid overflows
   #im1_gray = np.sum(im1.astype('float'), axis=2)
   #im2_gray = np.sum(im2.astype('float'), axis=2)
   im1_gray=im1_gray.astype('float')
   im2_gray=im2_gray.astype('float')

   # get rid of the averages, otherwise the results are not good
   im1_gray -= np.mean(im1_gray)
   im2_gray -= np.mean(im2_gray)

   # calculate the correlation image; note the flipping of onw of the images
   corr_img=scipy.signal.fftconvolve(im1_gray, im2_gray[::-1,::-1], mode='same')
   ShiftIndices=np.unravel_index(np.argmax(corr_img), corr_img.shape)
   #return [ShiftIndices[0], ShiftIndices[1]] 
   return [ShiftIndices[0]-(corr_img.shape[0]/2), ShiftIndices[1]-(corr_img.shape[1]/2)]


def FindHomogrpahy(pts_pts_src, pts_dst):
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
     
    # Warp source image to destination based on homography
    im_out = cv2.warpPerspective(im_src, h, (im_dst.shape[1],im_dst.shape[0]))
     

def RegisterChannels(Viewer):
	Display=Viewer.display
	#Get Confocal Image
	ConfocalIndex=0
	for ind in range(len(Display.ConfocalChannelVisible)):
		if Display.ConfocalChannelVisible[ind]==True:
			ConfocalIndex=ind
	ConfocalImg=Display.ConfChannelToShow[ConfocalIndex]
	#rotate 90 and flip to bring into correct position
	Scale=GlobalDownscale
	ConfocalImg = cv2.resize(ConfocalImg, (0,0), fx=1.0/Scale , fy=1.0/Scale)
	(h, w) = ConfocalImg.shape[:2]
	center = (w / 2, h / 2)
	M = cv2.getRotationMatrix2D(center, 0, 1.0)
	ConfocalImg = cv2.warpAffine(ConfocalImg, M, (w, h))
	#print ConfocalImg.shape
	cv2.imwrite('confocal.png',ConfocalImg)
	#Get Strom Image0
	StormIndex=0
	for ind in range(len(Display.StormChannelVisible)):
		if Display.StormChannelVisible[ind]==True:
			StormIndex=ind
	
	#recalculate strom image in confocal
	Scale=100.0/Display.ConfocalSizeMultiplier
	Gausses = np.array(Display.StormData_filtered[StormIndex])
	MaxSizeX=int(np.ndarray.max(Gausses[:, 0])/(Scale*Display.ConfocalMetaData['SizeX']*GlobalDownscale))
	MaxSizeY=int(np.ndarray.max(Gausses[:, 1])/(Scale*Display.ConfocalMetaData['SizeX']*GlobalDownscale))

	StormImg=np.zeros((MaxSizeX+1,MaxSizeY+1))
	#print StormImg.shape
	for a in range(len(Gausses)):
   		#this could be changed to where-indexing, instead of append
   		IndX=int(Gausses[a, 0]/(Scale*Display.ConfocalMetaData['SizeX']*GlobalDownscale))
   		IndY=int(Gausses[a, 1]/(Scale*Display.ConfocalMetaData['SizeX']*GlobalDownscale))
		StormImg[IndX][IndY]=255
	StormImg = cv2.resize(StormImg, (0,0), fx=1.0/Scale , fy=1.0/Scale)	
	(h, w) = StormImg.shape[:2]
	center = (w / 2, h / 2)
	M = cv2.getRotationMatrix2D(center, 90, 1.0)
	StormImg = cv2.warpAffine(StormImg, M, (w, h))
	StormImg= c=cv2.flip(StormImg,0)
	cv2.imwrite('stromg.png',StormImg)	
	
	#register the two images
	#cut out middle of storm image
	MidX = StormImg.shape[0]/2
	MidY = StormImg.shape[1]/2

	CutStormImg= StormImg[(MidX-(ConfocalImg.shape[0]/2)):(MidX+(ConfocalImg.shape[0]/2)),(MidY-(ConfocalImg.shape[1]/2)):(MidY+(ConfocalImg.shape[1]/2))]
	#Rescale=1.17857142
	#StormImg=cv2.resize(StormImg,None,fx=1.0/Rescale, fy=1.0/Rescale)
	#set the shift between the iamges accordingly
	Shift=cross_image(CutStormImg, ConfocalImg)
	CutOutX=(StormImg.shape[0]-CutStormImg.shape[0])/2
	CutOutY=(StormImg.shape[1]-CutStormImg.shape[1])/2
	#print Shift[0]+CutOutX
	#print Shift[1]+CutOutY
	ImgShift=[(Shift[0]+CutOutX)*(Scale*Display.ConfocalMetaData['SizeX']*GlobalDownscale), (Shift[1]+CutOutY)*(Scale*Display.ConfocalMetaData['SizeY']*GlobalDownscale)] 
	#print ImgShift
	#move image back to origin
	Display.DisplayedConfocalChannel[ConfocalIndex].translate( -Display.Viewbox.ConfocalOffset[0],-Display.Viewbox.ConfocalOffset[1])
	#move image to correct position
	Display.DisplayedConfocalChannel[ConfocalIndex].translate( ((Shift[1]+CutOutY)*Scale), ((Shift[0]+CutOutX)*Scale))
	Display.Viewbox.ConfocalOffset= [((Shift[1]+CutOutY)*Scale), ((Shift[0]+CutOutX)*Scale)]
	rows,cols = ConfocalImg.shape
	M = np.float32([[1,0,Shift[1]],[0,1,Shift[0]]])
	ConfImg = cv2.warpAffine(ConfocalImg,M,(cols,rows))
	
	Height=StormImg.shape[0]
	Width=StormImg.shape[1]
	out_image = np.zeros((Height,Width,3), np.uint8)

	out_image[0:StormImg.shape[0],0:StormImg.shape[1],2]=StormImg
	ShitfX=(StormImg.shape[0]-CutStormImg.shape[0])/2
	ShiftY=(StormImg.shape[1]-CutStormImg.shape[1])/2
	#print ShitfX
	#print ConfocalImg.shape[0]+ShitfX
	#out_image[ShitfX:(ConfocalImg.shape[0]+ShitfX),ShiftY:(ShiftY+ConfocalImg.shape[1]),1]=ConfocalImg
	#cv2.imwrite('reg_test.jpg',out_image)
	#call iteratively in the middle

