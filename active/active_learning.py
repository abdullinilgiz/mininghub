import os
from pathlib import Path

import torch
import numpy as np
import cv2

ROOT_DIR = Path(__file__).resolve().parent.parent
FRAME_RATE = 24
CONF_TRESHOLD = 0.8
VIDEO_PATH = os.path.join(ROOT_DIR, 'data', '20sec_day.mp4')

model = torch.hub.load(
    'ultralytics/yolov5',
    'custom',
    path=os.path.join(ROOT_DIR, 'models', 'YOLO_signs.pt'),
    force_reload=True
)


def convert_to_yolo(x1, y1, x2, y2, image_width=1280, image_height=960):
    x = (x1 + x2) / (2 * image_width)
    y = (y1 + y2) / (2 * image_height)
    w = (x2 - x1) / image_width
    h = (y2 - y1) / image_height
    return x, y, w, h


cap = cv2.VideoCapture(VIDEO_PATH)
frame_count = -1
unique_id = 0
ACTIVE_DIR = os.path.join(ROOT_DIR, 'data', 'active')

while cap.isOpened():
    ret, frame = cap.read()
    image_height, image_width, _ = frame.shape
    frame_count += 1
    print(frame_count)
    if not ret:
        break

    if frame_count % FRAME_RATE != 0:
        continue

    results = model(frame)
    confs = list()
    labels = ''
    for det in results.xyxy[0]:  # Перебираем все детекции
        class_id = int(det[-1])
        confidence = float(det[-2])
        confs.append(confidence)
        bbox = det[:4].cpu().numpy()
        x, y, w, h = convert_to_yolo(
            bbox[0], bbox[1], bbox[2], bbox[3],
            image_width=image_width,
            image_height=image_height)
        labels += f"{class_id} {x} {y} {w} {h}\n"

    is_confident = True
    for conf in confs:
        if conf < CONF_TRESHOLD:
            is_confident = False
    if is_confident:
        conf_dir = os.path.join(ACTIVE_DIR, 'confident')
    else:
        conf_dir = os.path.join(ACTIVE_DIR, 'not_confident')

    unique_id += 1
    cv2.imwrite(os.path.join(conf_dir, f'frame_{unique_id}.png'), frame)

    with open(os.path.join(conf_dir, f'frame_{unique_id}.txt'), 'w') as file:
        file.write(labels)

    cv2.imshow('YOLO', np.squeeze(results.render()))

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
