from subprocess import check_output
import glob
import os
import numpy as np
import cv2


# Run SAM on the frame folder
def run_sam():
    check_output(["python", "sam/main.py", "test", "frame/"])


def find_focus_rect(image_name):
	image = cv2.imread(image_name)
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(image_gray, 127, 255, 0)
	#print ret,thresh

	im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#print contours[0]
	for i in contours:
		x,y,w,h = cv2.boundingRect(i)
		print x,y,w,h,
	print
	return


def main(directory_name="predictions/"):
    for filename in list(glob.glob(os.path.join(directory_name, '*.jpg'))):
        find_focus_rect(filename)


main()
