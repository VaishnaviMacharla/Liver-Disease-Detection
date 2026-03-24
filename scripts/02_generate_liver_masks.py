import os
import json
import cv2
import numpy as np

LABELS_DIR = "../data/raw/Project_last/Labels"
OUTPUT_DIR = "../data/masks"

CLASSES = ["Grade_1", "Grade_2", "Healthy"]

def json_to_mask(json_path, image_shape):
    """
    Converts outline JSON (list of [x,y]) to liver mask
    """
    mask = np.zeros(image_shape[:2], dtype=np.uint8)

    with open(json_path, "r") as f:
        points = json.load(f)

    # Expecting: [[x1,y1], [x2,y2], ...]
    if not isinstance(points, list) or len(points) < 3:
        return mask

    polygon = np.array(points, dtype=np.int32)
    cv2.fillPoly(mask, [polygon], 255)

    return mask


for cls in CLASSES:
    print(f"\n🩻 Processing liver masks for: {cls}")

    img_dir = os.path.join(LABELS_DIR, cls, "image")
    json_dir = os.path.join(LABELS_DIR, cls, "segmentation", "outline")
    save_dir = os.path.join(OUTPUT_DIR, cls, "liver")

    os.makedirs(save_dir, exist_ok=True)

    for json_file in os.listdir(json_dir):
        if not json_file.endswith(".json"):
            continue

        base_name = os.path.splitext(json_file)[0]
        image_path = os.path.join(img_dir, base_name + ".jpg")

        if not os.path.exists(image_path):
            print(f"⚠️ Image not found for {base_name}")
            continue

        image = cv2.imread(image_path)
        if image is None:
            print(f"⚠️ Failed to load image {base_name}")
            continue

        mask = json_to_mask(os.path.join(json_dir, json_file), image.shape)

        save_path = os.path.join(save_dir, base_name + ".png")
        cv2.imwrite(save_path, mask)

    print(f"✅ Liver masks generated for {cls}")

print("\n🎉 STEP 3 COMPLETED SUCCESSFULLY")
