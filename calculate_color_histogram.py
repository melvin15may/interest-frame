import cv2
from matplotlib import pyplot as plt
import numpy as np

"""
This code is a modification of code here: http://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_image_histogram_calcHist.php
"""


def get_histogram(cv2_image):
    color = ('b', 'g', 'r')
    histogram = []  # histogram in blue,green,red sequence
    for channel in range(0, 1):
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

"""
def compare_histogram(frame1, frame2, distance_type=cv2.HISTCMP_BHATTACHARYYA):
    return cv2.compareHist(np.array(get_histogram(frame1)), np.array(get_histogram(frame2)), distance_type)
"""


def is_key_frame(color_histogram, frame, frame_number, threshold):
    frame_hist = get_histogram(frame)
    mean_hist_diff = sum(sum(subtract_histograms(
        color_histogram / (frame_number * 1.0), frame_hist)))
    if mean_hist_diff > threshold:
        color_histogram = frame_hist
        key_frame = True
    else:
        color_histogram = add_histograms(color_histogram, frame_hist)
        key_frame = False
    return key_frame, color_histogram


def compare_histogram_from_file(file_name1, file_name2, distance_type=cv2.HISTCMP_BHATTACHARYYA):
    return cv2.compareHist(np.array(get_histogram(read_image(file_name1))), np.array(get_histogram(read_image(file_name2))), distance_type)


def add_histograms(hist1, hist2):
    return np.array(hist1) + np.array(hist2)


def subtract_histograms(hist1, hist2):
    return abs(np.array(hist1) - np.array(hist2))


def mean_histogram_value():
    return abs


import sys


def main():
    # print(get_histogram(read_image(sys.argv[1])))
    img = read_image(sys.argv[1])
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(img_yuv)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, img_yuv)
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YCR_CB2BGR)
    cv2.imshow("hello", img)
    cv2.imshow("hello2", img_yuv)
    cv2.imshow("hello3", img_output)
    cv2.waitKey(0)

#main()
