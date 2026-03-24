import os
import cv2
import numpy as np

# Paths
IMAGE_DIR = "../data/raw/Project_last/Labels"
MASK_DIR = "../data/masks"
OUTPUT_DIR = "../data/processed"

CLASSES = ["Grade_1", "Grade_2", "Healthy"]

IMG_SIZE = 224  # for CNN compatibility

for cls in CLASSES:
    print(f"\n🧠 Extracting liver ROI for: {cls}")

    img_folder = os.path.join(IMAGE_DIR, cls, "image")
    mask_folder = os.path.join(MASK_DIR, cls, "liver")
    save_folder = os.path.join(OUTPUT_DIR, cls)

    os.makedirs(save_folder, exist_ok=True)

    for file in os.listdir(img_folder):
        if not file.lower().endswith(".jpg"):
            continue

        img_path = os.path.join(img_folder, file)
        mask_path = os.path.join(mask_folder, file.replace(".jpg", ".png"))

        if not os.path.exists(mask_path):
            print(f"⚠️ Mask missing for {file}")
            continue

        image = cv2.imread(img_path)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        if image is None or mask is None:
            print(f"⚠️ Failed to load {file}")
            continue

        # Apply mask
        liver_only = cv2.bitwise_and(image, image, mask=mask)

        # Crop bounding box
        coords = cv2.findNonZero(mask)
        x, y, w, h = cv2.boundingRect(coords)
        liver_crop = liver_only[y:y+h, x:x+w]

        # Resize for model
        liver_crop = cv2.resize(liver_crop, (IMG_SIZE, IMG_SIZE))

        # Save
        save_path = os.path.join(save_folder, file)
        cv2.imwrite(save_path, liver_crop)

    print(f"✅ ROI extraction completed for {cls}")

print("\n🎉 STEP 4 COMPLETED SUCCESSFULLY")
