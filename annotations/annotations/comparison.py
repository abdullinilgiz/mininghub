import os
from pathlib import Path


def parse_annotation_file(file_path):
    annotations_by_class = {}

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 5:
                class_id = int(parts[0])
                values = list(map(float, parts[1:]))
                annotations_by_class.setdefault(class_id, []).append(values)

    result = {}
    for class_id, annotations in annotations_by_class.items():
        result[class_id] = annotations

    return result


def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    top_left_x = max(x1, x2)
    top_left_y = max(y1, y2)
    bottom_right_x = min(x1 + w1, x2 + w2)
    bottom_right_y = min(y1 + h1, y2 + h2)

    if top_left_x < bottom_right_x and top_left_y < bottom_right_y:
        intersection_area = (bottom_right_x -
                             top_left_x) * (bottom_right_y - top_left_y)
        union_area = w1 * h1 + w2 * h2 - intersection_area
        iou = intersection_area / union_area
    else:
        iou = 0

    return iou


def compute_iou_for_annotations(annotations1, annotations2):
    class_ious = dict()
    for class_id, boxes1 in annotations1.items():
        if class_id in annotations2:
            boxes2 = annotations2[class_id]
            for box1 in boxes1:
                max_iou = 0
                for box2 in boxes2:
                    iou = calculate_iou(box1, box2)
                    if iou > max_iou:
                        max_iou = iou
                class_ious.setdefault(class_id, []).append(max_iou)
    return class_ious


directory_name = Path(__file__).resolve().parent

annot1_path = os.path.join(directory_name, 'labels_me')
annot2_path = os.path.join(directory_name, 'labels_annotator')

annotations1 = set(os.listdir(annot1_path))
annotations2 = set(os.listdir(annot2_path))

signs_missed = 0
sign_amount = 0
iou_sum = 0
for ann in annotations1:
    if ann not in annotations2:
        raise FileNotFoundError(f'File do not exist in {annot2_path}')
    file_path = os.path.join(annot1_path, ann)
    annot1 = parse_annotation_file(file_path)
    file_path = os.path.join(annot2_path, ann)
    annot2 = parse_annotation_file(file_path)
    class_ious1 = compute_iou_for_annotations(annot1, annot2)
    class_ious2 = compute_iou_for_annotations(annot2, annot1)
    for key, values in class_ious1.items():
        for value in values:
            if value != 0:
                sign_amount += 1
                iou_sum += value
            else:
                signs_missed += 1
    for key, values in class_ious2.items():
        for value in values:
            if value == 0:
                signs_missed += 1

print('Количество совпадающих знаков:', sign_amount)
print('Среднее знакчение метрики IoU для этих знаков:',
      round(iou_sum / sign_amount, 3))
print('Количество пропущенных знаков:', signs_missed)
