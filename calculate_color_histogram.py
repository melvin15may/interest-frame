import cv2
from matplotlib import pyplot as plt
import numpy as np

"""
This code is a modification of code here: http://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_image_histogram_calcHist.php
"""


def get_histogram(cv2_image):
    color = ('b', 'g', 'r')
    histogram = []  # histogram in blue,green,red sequence

    # Equalize histogram
    cv2_ycrcb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2YCR_CB)  # or convert
    channels = cv2.split(cv2_ycrcb)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, cv2_ycrcb)
    cv2_image = cv2.cvtColor(cv2_ycrcb, cv2.COLOR_YCR_CB2BGR)

    for channel in range(0, 3):
        # cv2.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
        # channel:  if input is grayscale image, its value is [0]. For color
        # 			image, you can pass [0],[1] or [2] to calculate histogram of
        # 			blue,green or red channel, respectively
        hist = cv2.calcHist([cv2_image], [channel], None, [256], [0, 256])
        #cv2.normalize(hist, hist, 0, 256, cv2.NORM_MINMAX)
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


def compare_histogram(frame1, frame2, distance_type=cv2.HISTCMP_BHATTACHARYYA):
    return cv2.compareHist(np.array(get_histogram(frame1)), np.array(get_histogram(frame2)), distance_type)


def compare_histogram_from_file(file_name1, file_name2, distance_type=cv2.HISTCMP_BHATTACHARYYA):
    return cv2.compareHist(np.array(get_histogram(read_image(file_name1))), np.array(get_histogram(read_image(file_name2))), distance_type)
