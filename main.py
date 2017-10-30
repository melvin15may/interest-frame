import calculate_color_histogram as cch
import sys
import cv2
import os


def write_interest_frame(file_name, output_file_name):
	print file_name
	frames = []
	video_file = cv2.VideoCapture(file_name)
	while video_file.isOpened():
		ret, frame = video_file.read()
		if frame is not None:
			frames.append(frame)
		if not ret:
			break

	min_distance = float('inf')
	min_frame = frames[0]
	for frame1 in frames:
		d = 0
		for frame2 in frames:
			d += cch.compare_histogram(frame1, frame2)
		if min_distance > d:
			min_distance = d
			min_frame = frame1

	cv2.imwrite(sys.argv[1] + "frame/"+ output_file_name +".jpg", min_frame)


def main():
    for filename in os.listdir(sys.argv[1]):
        write_interest_frame(sys.argv[1] + filename, filename)

main()
