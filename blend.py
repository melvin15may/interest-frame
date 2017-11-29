from subprocess import check_output
import glob
import os
import numpy as np
import cv2
import json
from seam_carving import SeamCarver
import sys
from PIL import Image
from tqdm import tqdm
import argparse
import pyramid

def write_file(file_name, image):
    cv2.imwrite(file_name, image)


# Run SAM on the frame folder
def run_sam(sam_directory, directory_name="frame_key/"):
    check_output(["python", os.path.join(
        sam_directory, "main.py"), "test", directory_name])


def crop_image(image):
    return image[42:40 + 206, :]


def remove_black_bars(image):
    delete_index = []
    count = 0
    for row in image:
        shape_valid = row[np.logical_not(np.logical_and(
            row[:, 0] == 0, row[:, 1] == 0, row[:, 2] == 0))]
        if shape_valid.shape[0] == 0:
            delete_index.append(count)
        count += 1
    return np.delete(image, delete_index, axis=0)


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
    # image_masked = cv2.bitwise_and(image, image, mask=im2)
    # cv2.imshow(image_name, image)
    # cv2.waitKey(0)
    """
    for i in contours:
        x, y, w, h = cv2.boundingRect(i)
        print x, y, w, h,
    """
    return image, im2


def create_tapestery(data, frame_directory_name="interest_frame/", saliency_directory_name="predictions/", width_reduction=0.6, height_reduction=0.85):

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
                frame_directory_name, key), saliency_image_name=os.path.join(saliency_directory_name, key))
            #image, image_mask = test.get_sal(image_name=os.path.join(frame_directory_name, key))
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

            if image_vertical is None:
                image_vertical = image
                image_mask_vertical = image_mask
                frame_map_vertical = buffer_map
            else:
                #image_vertical = np.concatenate((image_vertical, image), axis=0)
                image_vertical = pyramid.pyramid_blend(image_vertical, image, axis=0)
                image_mask_vertical = np.concatenate(
                    (image_mask_vertical, image_mask), axis=0)
                frame_map_vertical = np.concatenate(
                    (frame_map_vertical, buffer_map), axis=0)
            image_vertical_count += 1

            if image_vertical_count == 3:
                if image_horizontal is None:
                    image_horizontal = image_vertical
                    image_mask_horizontal = image_mask_vertical
                    frame_map_horizontal = frame_map_vertical
                else:
                    #image_horizontal = np.concatenate((image_horizontal, image_vertical), axis=1)
                    image_horizontal = pyramid.pyramid_blend(image_horizontal, image_vertical, axis=1)
                    image_mask_horizontal = np.concatenate(
                        (image_mask_horizontal, image_mask_vertical), axis=1)
                    frame_map_horizontal = np.concatenate(
                        (frame_map_horizontal, frame_map_vertical), axis=1)
                image_vertical = None
                image_mask_vertical = None
                frame_map_vertical = None
                image_vertical_count = 1
            # row += 352

        # cv2.imshow("combine", image_vertical)
        # cv2.waitKey(0)
        cv2.imwrite("combined_image_p_{}.jpg".format(ind), image_horizontal)
        cv2.imwrite("combined_image_mask_p_{}.jpg".format(
            ind), image_mask_horizontal)

        print("Image resizing for rank", ind)
        #image_resize_with_mask("combined_image_p_{}.jpg".format(ind), "combined_image_new_p_{}.jpg".format(ind), int(image_horizontal.shape[
        #    0] * height_reduction), int(image_horizontal.shape[1] * width_reduction), "combined_image_mask_p_{}.jpg".format(ind), frame_map_horizontal, "frame_map_{}.csv".format(ind))


def pretty_print(ar):

    row = ar.shape[0]
    col = ar.shape[1]

    for i in range(0, row):
        print("")
        for j in range(0, col):
            print(ar[i, j],)


def image_resize_with_mask(filename_input, filename_output, new_height, new_width, filename_mask, data, frame_map_file):
    obj = SeamCarver(filename_input, new_height, new_width,
                     protect_mask=filename_mask, frame_map=data, frame_map_file=frame_map_file)
    obj.save_result(filename_output)


def blend():

    parser = argparse.ArgumentParser(description='Create tapestry')
    parser.add_argument('-l', dest="load_frames",
                        help="Load frames from .rgb video (Default: False)", action='store_true', default=False)
    parser.add_argument('-e', dest="extract_frames",
                        help="Extract key frames from .rgb frames (Default: False)", action='store_true', default=False)
    parser.add_argument('-s', dest="sam", help="Execute SAM (Default: False)",
                        action='store_true', default=False)
    parser.add_argument('--video', dest='video',
                        help=".rgb video file", type=str)
    parser.add_argument('--json', dest='json',
                        help="JSON key frame file", type=str)
    parser.add_argument('--width_reduction', dest='width_reduction',
                        help="Width reduction factor (Default: 0.6)", nargs='?', type=float, default=0.6)
    parser.add_argument('--height_reduction', dest='height_reduction',
                        help="Height reduction factor (Default: 0.85)", nargs='?', type=float, default=0.8)
    parser.add_argument(
        '--frames_directory', dest='frames_directory', help="Directory to save frames from .rgb video file (Default: frame)", default="frame/",  nargs='?', type=str)
    parser.add_argument('--key_frames_directory', dest='key_frames_directory',
                        help="Directory to save key frames from .rgb video file (Default: frame_key)", nargs='?', default="frame_key/", type=str)
    parser.add_argument('--sam_directory', dest='sam_directory', help="Directory to SAM (Default: ../sam)",
                        nargs='?', default=os.path.join("..", "sam"), type=str)
    args = parser.parse_args()

    data_file = args.json  # JSON data file
    directory_name = args.frames_directory  # directory to save image file/frame
    video_file = args.video  # video file

    with open(data_file, 'r') as fp:
        data = json.load(fp)

    raw = np.fromfile(video_file, dtype=np.uint8)
    frame_dimension = 352 * 288 * 3
    timecoded = raw.reshape(-1, frame_dimension)

    if args.load_frames:
        print("Extracting frames from file")
        for t in tqdm(range(0, timecoded.shape[0])):
            colorcoded = timecoded[t].reshape(3, 288, 352)
            rgb = colorcoded.swapaxes(0, 2).swapaxes(0, 1)
            img = Image.fromarray(rgb)
            img.save(os.path.join(directory_name, "fig{0:08d}.jpg".format(t)))
    # Save frames
    if args.extract_frames:
        print("Removing TOP and BOTTOM black bars")
        for i in data:
            image = crop_image(cv2.imread(os.path.join(directory_name, i)))
            # cv2.imshow(i,image)
            # cv2.waitKey(0)
            #image = cv2.imread(os.path.join(directory_name, i))
            write_file(os.path.join(args.key_frames_directory, i), image)

    if args.sam:
        print("Running SAM")
        run_sam(args.sam_directory, args.key_frames_directory)
        print("Saving Saliency to predictions/")

    print("Create tapestery")
    create_tapestery(data, frame_directory_name=args.key_frames_directory,
                     width_reduction=args.width_reduction, height_reduction=args.height_reduction)


blend()
