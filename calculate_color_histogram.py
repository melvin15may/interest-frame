import sys
import cv2
from matplotlib import pyplot as plt
import numpy as np

"""
This code is a modification of code here: http://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_image_histogram_calcHist.php
"""


def get_histogram(cv2_image):
    color = ('b', 'g', 'r')
    histogram = []  # histogram in blue,green,red sequence
    for channel in range(0, 3):
        # cv2.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
        # channel:  if input is grayscale image, its value is [0]. For color
        # 			image, you can pass [0],[1] or [2] to calculate histogram of
        # 			blue,green or red channel, respectively
        hist = cv2.calcHist([cv2_image], [channel], None, [256], [0, 256])
        cv2.normalize(hist, hist, 0, 256, cv2.NORM_MINMAX)
        histogram.append(hist)
    return histogram


def read_image(file_name):
    img = cv2.imread(file_name, -1)
    return img


def plot_histogram(data):
    color = ('b', 'g', 'r')
    for channel, col in enumerate(color):
        plt.plot(data[channel], color=col)
        plt.xlim([0, 256])
    plt.title('Histogram for color scale picture')
    plt.show()


def compare_histogram(frame1=read_image(sys.argv[1]), frame2=read_image(sys.argv[2]), distance_type=cv2.HISTCMP_BHATTACHARYYA):
    return cv2.compareHist(np.array(get_histogram(frame1)), np.array(get_histogram(frame2)), distance_type)


#print compare_histogram()
