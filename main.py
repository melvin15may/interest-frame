import calculate_color_histogram as cch
import scenes
import sys
import cv2
import os
import json
import image_hash as has
from datetime import datetime
from collections import defaultdict

# threshold should be changed later
RANK_THRESHOLD = 0.33
SCENE_THRESHOLD = 35
BLUR_THRESHOLD = 100


def remove_similar_frame(start_frame, frames):
    frame_count = start_frame
    sorted_frames_numbers = []
    hash_code_count = defaultdict(int)
    hash_code_frame = defaultdict(list)
    hash_code_frame_blur = defaultdict(list)
    for frame1 in frames:
        blur_var = has.get_blur(frame=frame1)
        if blur_var <= BLUR_THRESHOLD:
            continue
        hash_code_count, hash_code = has.compare_images(frame=frame1, frames=hash_code_count)
        hash_code_frame_blur[hash_code].append(blur_var)
        
        # Dont take repititions
        if not hash_code in hash_code_frame:
            sorted_frames_numbers.append(frame1)

        hash_code_frame[hash_code].append(frame_count)
        frame_count += 1

    # sort based on similar images
    
    """
    for key in sorted(hash_code_count, key=hash_code_count.__getitem__):
        try:
            sorted_frames_numbers += [frames[x - start_frame] for _, x in sorted(zip(hash_code_frame_blur[key], hash_code_frame[key]))]
        except IndexError:
            pass
    """
    return sorted_frames_numbers


def write_interest_frame(start_frame, frames):
    frame_numbers = []
    frame_distances = []
    frame_count = start_frame

    for frame1 in frames:
        d = 0
        for frame2 in frames:
            d += cch.compare_histogram(frame1, frame2)
        frame_numbers.append(frame_count)
        frame_distances.append(d)
        frame_count += 1

    sorted_frames_numbers = sorted(zip(frame_distances, frame_numbers))
    sorted_frames_distances = sorted(frame_distances)
    # remove write func later
    # cv2.imwrite("frame/" + output_file_name + ".jpg", min_frame)
    # Format for sorted_frame_numbers => [(<distance>,<frame_number>)]
    return sorted_frames_numbers  # , sorted_frame_distances


def divide_video(frames, split_frames, fps):

    current_scene = 0
    start_frame = 0

    interest_frames = []
    json_output = []

    for f in split_frames:
        print datetime.now(),start_frame,f
        non_similar_frames = remove_similar_frame(
            start_frame=start_frame, frames=frames[start_frame:f])
        print datetime.now(),(f - start_frame), len(non_similar_frames)
        print "-----------------------------------"
        interest_frame = write_interest_frame(start_frame=start_frame, frames=non_similar_frames)
        """
        json_output.append({
            "timeframe": interest_frame / float(fps),
            "rank": rank
        })
        """
        interest_frames.append(interest_frame)
        current_scene += 1
        start_frame = f

    return interest_frames


def read_file(file_name):
    frames = []
    video_file = cv2.VideoCapture(file_name)
    while video_file.isOpened():
        ret, frame = video_file.read()
        if frame is not None:
            frames.append(frame)
        if not ret:
            break
    return frames


def main():
    scenes_data = scenes.get_frames(input_file_name=sys.argv[
                                    1], threshold=SCENE_THRESHOLD, output_file_name=None)  # output_file_name="output.avi"
    frames = read_file(file_name=sys.argv[1])
    interest_frames = divide_video(frames=frames, split_frames=scenes_data[
                                   'frames'], fps=scenes_data['fps'])
    json_output = []

    json_index = 1
    frames_added = []
    # print(interest_frames)
    for i in range(0, 10):
        print "threshold", (RANK_THRESHOLD / (i + 1))
        for ind, scene_frames in enumerate(interest_frames):
            try:
                for j in range(0, i + 1):
                    similar = False
                    for fa in frames_added:
                        distance = cch.compare_histogram(
                            frames[fa], frames[scene_frames[j][1]])
                        if distance < (RANK_THRESHOLD / (i + 1)):
                            similar = True
                            break
                    if not similar:
                        json_output.append({
                            "t": scene_frames[j][1] / float(scenes_data['fps']),
                            "r": 10 - i
                        })
                        frames_added.append(scene_frames[j][1])
                        cv2.imwrite(
                            "frame/fig{0:08d}.jpg".format(json_index), frames[scene_frames[j][1]])
                        json_index += 1
                        break
            except IndexError:
                pass

    with open('data.txt', 'w') as outfile:
        json.dump(json_output, outfile)

main()


def testing():
    print(cch.compare_histogram_from_file(sys.argv[1], sys.argv[2]))

# testing()
