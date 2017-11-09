import calculate_color_histogram as cch
import scenes
import sys
import cv2
import os
import json


def write_interest_frame(start_frame, frames, output_file_name):
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
        print start_frame, f
        interest_frame = write_interest_frame(start_frame=start_frame, frames=frames[
                                              start_frame:f], output_file_name='test' + str(current_scene))
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
                                    1], threshold=28, output_file_name=None)
    frames = read_file(file_name=sys.argv[1])
    interest_frames = divide_video(frames=frames, split_frames=scenes_data[
                                   'frames'], fps=scenes_data['fps'])
    json_output = []
    for scene_frames in interest_frames:
        print len(scene_frames)
        for i in range(0, 10):
            try:
                json_output.append({
                    "timeframe": scene_frames[i][1] / float(scenes_data['fps']),
                    "rank": 10 - i
                })
                cv2.imwrite(
                    "frame/fig{0:08d}.jpg".format(scene_frames[i][1]), frames[scene_frames[i][1]])
            except IndexError:
                pass

    with open('data.txt', 'w') as outfile:
        json.dump(json_output, outfile)

    """
    for filename in os.listdir(sys.argv[1]):
        write_interest_frame(sys.argv[1] + filename, filename)
    """

main()
