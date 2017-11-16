import calculate_color_histogram as cch
import scenes
import sys
import cv2
import os
import json


def remove_similar_frame(start_frame, frames):
    frame_count = start_frame
    sorted_frames_numbers = []
    hash_code_count = defaultdict(int)
    hash_code_frame = defaultdict(int)
    hash_code_frame_blur = defaultdict(int)
    for frame1 in frames:
        blur_var = has.get_blur(frame=frame1)
        if blur_var <= BLUR_THRESHOLD:
            continue
        hash_code_count, hash_code = has.compare_images(
            frame=frame1, frames=hash_code_count)

        # Dont take repititions
        if not hash_code in hash_code_frame:
            sorted_frames_numbers.append(frame1)
            if blur_var > hash_code_frame_blur[hash_code]:
                hash_code_frame_blur[hash_code] = blur_var
                hash_code_frame[hash_code] = frame_count

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
                                    1], threshold=30, output_file_name=None)
    frames = read_file(file_name=sys.argv[1])
    interest_frames = divide_video(frames=frames, split_frames=scenes_data[
                                   'frames'], fps=scenes_data['fps'])
    json_output = []

    json_index = 1
    frames_added = []

    # threshold should be changed later
    threshold = 0.3

    for i in range(0, 10):
        # print "threshold", (threshold / (i + 1))
        for ind, scene_frames in enumerate(interest_frames):
            try:
                similar = False
                for fa in frames_added:
                    distance = cch.compare_histogram(
                        frames[fa], frames[scene_frames[i][1]])
                    if distance < (threshold / (i + 1)):
                        similar = True
                        break
                if not similar:
                    json_output.append({
                        "t": scene_frames[i][1] / float(scenes_data['fps']),
                        "r": 10 - i
                    })
                    frames_added.append(scene_frames[i][1])
                    cv2.imwrite(
                        "frame/fig{0:08d}.jpg".format(json_index), frames[scene_frames[i][1]])
                    json_index += 1

            except IndexError:
                pass

    with open('data.txt', 'w') as outfile:
        json.dump(json_output, outfile)

main()


def testing():
    print cch.compare_histogram_from_file(sys.argv[1], sys.argv[2])

testing()
