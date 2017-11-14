from collections import defaultdict
import imagehash
import cv2


def compare_images(frame, frames=defaultdict(int), hashfunc=imagehash.phash):
	hash_code = hashfunc(frame)
	frames[hash_code] += 1
	return frames, hash_code


# blur detection
# https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
def get_blur(frame):
	return cv2.Laplacian(frame,cv2.CV_64F).var()
