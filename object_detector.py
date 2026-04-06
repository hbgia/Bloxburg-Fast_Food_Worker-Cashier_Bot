import tensorflow as tf
import numpy as np
import input_manager

_MODEL = tf.saved_model.load('object_detector')
_INFER = _MODEL.signatures["serving_default"]

def detect_objects(frame):
    # Preprocess frame for model input (normalize and resize to 640x640)
    frame_input, preprocess_meta = input_manager.preprocess_image(frame, width=640, height=640)

    # Run inference
    input_tensor = tf.convert_to_tensor(frame_input, dtype=tf.float32)
    raw_results = _INFER(input_tensor)

    # 1. SavedModel signature trả về dict, cần lấy Tensor trước khi transpose.
    pred = raw_results["output_0"] if "output_0" in raw_results else next(iter(raw_results.values()))
    output = tf.transpose(pred, perm=[0, 2, 1]) # Convert to (1, 8400, 19)

    # 2. Tách tọa độ và điểm số (YOLOv8: 4 cột đầu là box, còn lại là scores)
    boxes_xywh = output[:, :, 0:4]
    probs = output[:, :, 4:]

    # 3. Chuyển đổi [x_center, y_center, w, h] sang [y_min, x_min, y_max, x_max]
    # Lưu ý: Cần chuẩn hóa hoặc tính toán dựa trên kích thước ảnh 640x640
    x_center, y_center, w, h = tf.split(boxes_xywh, 4, axis=-1)
    y_min = (y_center - h / 2) / 640
    x_min = (x_center - w / 2) / 640
    y_max = (y_center + h / 2) / 640
    x_max = (x_center + w / 2) / 640
    boxes_final = tf.concat([y_min, x_min, y_max, x_max], axis=-1)

    # 4. Áp dụng Combined NMS
    selected_indices = tf.image.combined_non_max_suppression(
        boxes=tf.expand_dims(boxes_final, axis=2), # Thêm chiều cho từng class
        scores=probs,
        max_output_size_per_class=100,
        max_total_size=100,
        iou_threshold=0.45,
        score_threshold=0.5
    )

    valid = int(selected_indices.valid_detections.numpy()[0])
    print("Valid detections:", valid)
    
    if valid <= 0:
        return []

    classes = selected_indices.nmsed_classes[0, :valid].numpy().astype(np.int32)

    # Convert boxes from normalized 640x640 letterbox space back to original screen space.
    boxes = selected_indices.nmsed_boxes[0, :valid].numpy()
    input_w = preprocess_meta["input_width"]
    input_h = preprocess_meta["input_height"]
    scale = preprocess_meta["scale"]
    pad_left = preprocess_meta["pad_left"]
    pad_top = preprocess_meta["pad_top"]
    orig_w = preprocess_meta["orig_width"]
    orig_h = preprocess_meta["orig_height"]

    boxes_px = np.zeros_like(boxes)
    boxes_px[:, 0] = boxes[:, 0] * input_h
    boxes_px[:, 1] = boxes[:, 1] * input_w
    boxes_px[:, 2] = boxes[:, 2] * input_h
    boxes_px[:, 3] = boxes[:, 3] * input_w

    boxes_px[:, [0, 2]] = (boxes_px[:, [0, 2]] - pad_top) / scale
    boxes_px[:, [1, 3]] = (boxes_px[:, [1, 3]] - pad_left) / scale

    boxes_px[:, [0, 2]] = np.clip(boxes_px[:, [0, 2]], 0, orig_h)
    boxes_px[:, [1, 3]] = np.clip(boxes_px[:, [1, 3]], 0, orig_w)

    detections = []
    for cls, box in zip(classes, boxes_px):
        y0, x0, y1, x1 = box.tolist()
        detections.append([int(cls), x0, y0, x1, y1])
    return detections