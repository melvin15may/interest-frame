from subprocess import check_output
import glob
import os
import numpy as np
import cv2
import json


# Run SAM on the frame folder
def run_sam():
    check_output(["python", "sam/main.py", "test", "frame/"])


def find_focus_rect(image_name, saliency_image_name):
    saliency_image = cv2.imread(saliency_image_name)
    saliency_image_gray = cv2.cvtColor(saliency_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(saliency_image_gray, 80, 255, cv2.THRESH_BINARY)
    # print ret,thresh

    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print contours[0]
    # cv2.imshow(image_name,im2)
    # cv2.waitKey(0)
    image = cv2.imread(image_name)
    image_masked = cv2.bitwise_and(image, image, mask=im2)
    cv2.imshow(image_name, image_masked)
    cv2.waitKey(0)
    """
    for i in contours:
        x, y, w, h = cv2.boundingRect(i)
        print x, y, w, h,
    """
    return image


def merge_images_col(img1, highest_y, img2, lowest_y):
    img1_height, img1_width, img1_channels = img1.shape
    img2_height, img2_width, img2_channels = img2.shape
    output_img_height = img1_height - highest_y + img2_height - lowest_y
    output_img_width = max(img2_width, img1_width)
    output_img = np.zeros((output_img_height, output_img_width, img1_channels))
    output_img[0:output_img_height] = img1
    
    return


def main(data_file="data.txt", directory_name="predictions/"):
    data = {}
    with open(data_file, 'r') as fp:
        data = json.load(fp)
    for ind, val in enumerate(data):
        if val['r'] == 10:
            image_masked = find_focus_rect(image_name=os.path.join("frame/", "fig{0:08d}.jpg".format(
                ind + 1)), saliency_image_name=os.path.join(directory_name, "fig{0:08d}.jpg".format(ind + 1)))
    #cv2.imshow("combine", images)
    # cv2.waitKey(0)

    """
    for filename in list(glob.glob(os.path.join(directory_name, '*.jpg'))):
        find_focus_rect(filename)
    """


main()
