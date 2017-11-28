from subprocess import check_output
import glob
import os
import numpy as np
import cv2
import json
from seam_carving import SeamCarver
from main import read_file, write_file
import sys


# Run SAM on the frame folder
def run_sam(directory_name="frame/"):
    check_output(["python", "sam/main.py", "test", directory_name])


def remove_black_bars(image):
    new_image = image[np.logical_not(np.logical_and(
        image[:, :, 0] == 0, image[:, :, 1] == 0, image[:, :, 2] == 0))]
    return new_image


def find_focus_rect(image_name, saliency_image_name):
    saliency_image = cv2.imread(saliency_image_name)
    saliency_image_gray = cv2.cvtColor(saliency_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(
        saliency_image_gray, 50, 255, cv2.THRESH_BINARY)
    # print ret,thresh

    im2, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print contours[0]
    # cv2.imshow(image_name,im2)
    # cv2.waitKey(0)
    image = cv2.imread(image_name)
    #image_masked = cv2.bitwise_and(image, image, mask=im2)
    #cv2.imshow(image_name, image)
    # cv2.waitKey(0)
    """
    for i in contours:
        x, y, w, h = cv2.boundingRect(i)
        print x, y, w, h,
    """
    return image, im2


def create_tapestery(data, directory_name="predictions/"):
    data = {}

    ranked_frames = [[], [], [], []]
    for key in data:
        ranked_frames[data[key]['r']].append(key)

    ranked_frames[0] = sorted(ranked_frames[0])
    for j in range(1, 4):
        ranked_frames[j] += ranked_frames[j - 1]
        ranked_frames[j] = sorted(ranked_frames[j])

    for ind, frames in enumerate(ranked_frames):
        print("Tapestry for RANK", ind)
        image_vertical = None
        image_mask_vertical = None
        image_horizontal = None
        image_mask_horizontal = None
        image_vertical_count = 1
        frame_map_horizontal = None
        frame_map_vertical = None
        for key in frames:
            image, image_mask = find_focus_rect(image_name=os.path.join(
                "frame/", key), saliency_image_name=os.path.join(directory_name, key))
            """
            if image_horizontal is not None:
                image_horizontal = np.concatenate(
                    (image_horizontal, image), axis=1)
                image_mask_horizontal = np.concatenate(
                    (image_mask_horizontal, image_mask), axis=1)
                buffer_map = np.empty((image.shape[0], image.shape[1]), dtype=int)
                buffer_map[:] = ind
                frame_map = np.concatenate((frame_map, buffer_map), axis=1)
            else:
                image_horizontal = image
                image_mask_horizontal = image_mask
                frame_map = np.empty(
                    (image.shape[0], image.shape[1]), dtype=int)
                frame_map[:] = ind
            """
            buffer_map = np.empty((image.shape[0], image.shape[1]), dtype=int)
            buffer_map[:] = int(key[7:11])
            if image_vertical_count == 3:
                if image_horizontal is None:
                    image_horizontal = image_vertical
                    image_mask_horizontal = image_mask_vertical
                    frame_map_horizontal = frame_map_vertical
                else:
                    image_horizontal = np.concatenate(
                        (image_horizontal, image_vertical), axis=1)
                    image_mask_horizontal = np.concatenate(
                        (image_mask_horizontal, image_mask_vertical), axis=1)
                    frame_map_horizontal = np.concatenate(
                        (frame_map_horizontal, frame_map_vertical), axis=1)
                image_vertical = image
                image_mask_vertical = image_mask
                frame_map_vertical = buffer_map
                image_vertical_count = 2
            else:
                if image_vertical is None:
                    image_vertical = image
                    image_mask_vertical = image_mask
                    frame_map_vertical = buffer_map
                else:
                    image_vertical = np.concatenate(
                        (image_vertical, image), axis=0)
                    image_mask_vertical = np.concatenate(
                        (image_mask_vertical, image_mask), axis=0)
                    frame_map_vertical = np.concatenate(
                        (frame_map_vertical, buffer_map), axis=0)
                image_vertical_count += 1
            #row += 352

        #cv2.imshow("combine", image_combine)
        # cv2.waitKey(0)
        cv2.imwrite("combined_image_{}.jpg".format(ind), image_horizontal)
        cv2.imwrite("combined_image_mask_{}.jpg".format(
            ind), image_mask_horizontal)

        print("Image resizing for rank", ind)
        image_resize_with_mask("combined_image_{}.jpg".format(ind), "combined_image_new_{}.jpg".format(ind), int(image_horizontal.shape[
            0] * 1.8 / 3), int(image_horizontal.shape[1] * 1.8 / 3), "combined_image_mask_{}.jpg".format(ind), frame_map_horizontal, "frame_map_{}.csv".format(ind))


def pretty_print(ar):

    row = ar.shape[0]
    col = ar.shape[1]

    for i in range(0, row):
        print ""
        for j in range(0, col):
            print ar[i, j],


def image_resize_with_mask(filename_input, filename_output, new_height, new_width, filename_mask, data, frame_map_file):
    obj = SeamCarver(filename_input, new_height, new_width,
                     protect_mask=filename_mask, frame_map=data, frame_map_file=frame_map_file)
    obj.save_result(filename_output)


def blend():
    data_file = sys.argv[2]  # JSON data file
    directory_name = sys.argv[3]  # directory to save image file/frame
    video_file = sys.argv[1]  # video file

    with open(data_file, 'r') as fp:
        data = json.load(fp)

    frames = read_file(video_file)
    print frames
    # Save frames
    print("Removing TOP and BOTTOM black bars")
    for i in data:
        image = remove_black_bars(cv2.imread(os.path.join(directory_name, i)))
        write_file(os.path.join(directory_name, i), image)

    print("Running SAM")
    run_sam(directory_name)

    print("Create tapestery")
    create_tapestery(data)


blend()
