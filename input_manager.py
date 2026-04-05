import mss
import numpy as np
import cv2


def _get_primary_monitor(sct):
    # Monitor containing coordinate origin (0, 0) is the primary display on Windows.
    for monitor in sct.monitors[1:]:
        left = monitor["left"]
        top = monitor["top"]
        right = left + monitor["width"]
        bottom = top + monitor["height"]
        if left <= 0 < right and top <= 0 < bottom:
            return monitor

    # Fallback to the first physical monitor if origin-based detection fails.
    return sct.monitors[1]

def take_full_screenshot():
    with mss.mss() as sct:
        raw_monitor = _get_primary_monitor(sct)

        screenshot = sct.grab(raw_monitor)

        # convert to numpy array
        frame = np.array(screenshot)

        # mss returns BGRA → convert to BGR
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    
def take_screen_region(x1, y1, x2, y2):
    width = int(x2 - x1)
    height = int(y2 - y1)
    if width <= 0 or height <= 0:
        raise ValueError("Invalid region: x2 must be > x1 and y2 must be > y1")

    monitor = {
        "left": int(x1),
        "top": int(y1),
        "width": width,
        "height": height,
    }

    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

def preprocess_image(frame, width: int, height: int):
    src_h, src_w = frame.shape[:2]
    scale = min(width / src_w, height / src_h)

    resized_w = int(round(src_w * scale))
    resized_h = int(round(src_h * scale))
    frame_resized = cv2.resize(frame, (resized_w, resized_h), interpolation=cv2.INTER_LINEAR)

    pad_w = width - resized_w
    pad_h = height - resized_h
    pad_left = pad_w // 2
    pad_right = pad_w - pad_left
    pad_top = pad_h // 2
    pad_bottom = pad_h - pad_top

    # Keep aspect ratio to avoid geometric distortion before inference.
    frame_letterboxed = cv2.copyMakeBorder(
        frame_resized,
        pad_top,
        pad_bottom,
        pad_left,
        pad_right,
        cv2.BORDER_CONSTANT,
        value=(114, 114, 114)
    )

    # Exported YOLO pipelines commonly expect RGB float32 in [0, 1].
    frame_rgb = cv2.cvtColor(frame_letterboxed, cv2.COLOR_BGR2RGB)
    frame_normalized = frame_rgb.astype(np.float32) / 255.0

    input_tensor = np.expand_dims(frame_normalized, axis=0).astype(np.float32)
    meta = {
        "orig_width": src_w,
        "orig_height": src_h,
        "input_width": width,
        "input_height": height,
        "scale": scale,
        "pad_left": pad_left,
        "pad_top": pad_top,
    }
    return input_tensor, meta