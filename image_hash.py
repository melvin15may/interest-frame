from collections import defaultdict
import imagehash
import cv2
from PIL import Image

def compare_images(frame, frames=defaultdict(int), hashfunc=imagehash.whash):
	hash_code = hashfunc(Image.fromarray(frame))
	frames[hash_code] += 1
	return frames, hash_code


# blur detection
# https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
def get_blur(frame):
	return cv2.Laplacian(frame,cv2.CV_64F).var()
