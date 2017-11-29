import numpy as np
import cv2

#image_name = "frame_key/fig00004825.jpg"
def get_sal(image_name):
	image_org = cv2.imread(image_name)
	image=image_org
	cv2.pyrMeanShiftFiltering(image, 2, 10, image, 4)

	def backproject(source, target, levels = 2, scale = 1):
		hsv = cv2.cvtColor(source,  cv2.COLOR_BGR2HSV)
		hsvt = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
		# calculating object histogram
		roihist = cv2.calcHist([hsv],[0, 1], None, [levels, levels], [0, 180, 0, 256] )

		# normalize histogram and apply backprojection
		cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
		dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256], scale)
		return dst

	backproj = np.uint8(backproject(image, image, levels = 2))

	cv2.normalize(backproj,backproj,0,255,cv2.NORM_MINMAX)

	saliencies = [backproj, backproj, backproj]
	saliency = cv2.merge(saliencies)
	cv2.pyrMeanShiftFiltering(saliency, 20, 200, saliency, 2)
	saliency = cv2.cvtColor(saliency, cv2.COLOR_BGR2GRAY)
	cv2.equalizeHist(saliency, saliency)

	(T, saliency) = cv2.threshold(saliency, 220, 255, cv2.THRESH_BINARY)
	im2, contours, hierarchy = cv2.findContours(saliency * 1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	return image_org,im2