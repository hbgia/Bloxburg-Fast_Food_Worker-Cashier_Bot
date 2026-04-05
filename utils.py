import cv2
import numpy as np


def load_image_as_array(filepath: str) -> np.ndarray:
	"""Load an image from disk and return it as a NumPy array."""
	if not filepath:
		raise ValueError("filepath must be a non-empty string")

	image = cv2.imread(filepath)
	if image is None:
		raise FileNotFoundError(f"Cannot read image from path: {filepath}")

	return image

def crop_frame_copy(frame, x1, y1, x2, y2):
    x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
    if x2 <= x1 or y2 <= y1:
        raise ValueError("Invalid box")
    return frame[y1:y2, x1:x2].copy()