import calculate_color_histogram as cch
import sys
import cv2


def main():
    frames = []
    video_file = cv2.VideoCapture(sys.argv[1])
    while video_file.isOpened():
        ret, frame = video_file.read()
        if frame is not None:
            frames.append(frame)
        if not ret:
            break

    min_distance = float('inf')
    min_distances = []
    for frame1 in frames:
    	d = 0
    	for frame2 in frames:
        	d += cch.compare_histogram(frame1, frame2)
        min_distances.append(d)

    cv2.imwrite("frame.jpg", frames[min_distances.index(min(min_distances))])

main()
