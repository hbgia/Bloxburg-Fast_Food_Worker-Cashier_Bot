import tensorflow as tf
import numpy as np
import cv2

_MODEL = tf.saved_model.load('quantity_and_size_classifier/model.savedmodel')
_INFER = _MODEL.signatures["serving_default"]

with open('quantity_and_size_classifier/labels.txt', 'r', encoding='utf-8') as f:
    _LABELS = [line.strip().split(maxsplit=1)[1] for line in f if line.strip()]


def _preprocess_teachable_machine(frame: np.ndarray, image_size: int = 224) -> np.ndarray:
    if frame is None or frame.size == 0:
        raise ValueError("Input frame is empty")

    src_h, src_w = frame.shape[:2]
    if src_h <= 0 or src_w <= 0:
        raise ValueError("Invalid frame dimensions")

    # Teachable Machine image models are typically trained with center-cropped RGB images.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    scale = max(image_size / src_w, image_size / src_h)
    resized_w = max(1, int(round(src_w * scale)))
    resized_h = max(1, int(round(src_h * scale)))
    resized = cv2.resize(frame_rgb, (resized_w, resized_h), interpolation=cv2.INTER_LINEAR)

    start_x = max(0, (resized_w - image_size) // 2)
    start_y = max(0, (resized_h - image_size) // 2)
    cropped = resized[start_y:start_y + image_size, start_x:start_x + image_size]
    if cropped.shape[0] != image_size or cropped.shape[1] != image_size:
        cropped = cv2.resize(cropped, (image_size, image_size), interpolation=cv2.INTER_LINEAR)

    normalized = (cropped.astype(np.float32) / 127.5) - 1.0
    return np.expand_dims(normalized, axis=0).astype(np.float32)

def classify_frame(frame): 
    input_batch = _preprocess_teachable_machine(frame, image_size=224)

    output_dict = _INFER(tf.convert_to_tensor(input_batch))
    output_tensor = next(iter(output_dict.values()))
    logits = output_tensor.numpy().squeeze()

    class_idx = int(np.argmax(logits))
    if class_idx < 0 or class_idx >= len(_LABELS):
        return str(class_idx)

    return _LABELS[class_idx]