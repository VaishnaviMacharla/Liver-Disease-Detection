import os
import shutil
import random

# Paths
SOURCE_DIR = "../data/processed"
TARGET_DIR = "../data/final"

# Split ratios
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

CLASSES = ["Grade_1", "Grade_2", "Healthy"]

random.seed(42)

for cls in CLASSES:
    print(f"\n📂 Processing class: {cls}")

    src_class_dir = os.path.join(SOURCE_DIR, cls)
    images = [f for f in os.listdir(src_class_dir) if f.lower().endswith(".jpg")]

    random.shuffle(images)

    total = len(images)
    train_end = int(TRAIN_RATIO * total)
    val_end = train_end + int(VAL_RATIO * total)

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split, files in splits.items():
        split_dir = os.path.join(TARGET_DIR, split, cls)
        os.makedirs(split_dir, exist_ok=True)

        for file in files:
            src_path = os.path.join(src_class_dir, file)
            dst_path = os.path.join(split_dir, file)
            shutil.copy(src_path, dst_path)

        print(f"✅ {split}: {len(files)} images")

print("\n🎉 STEP 4 COMPLETED: Dataset successfully split into Train / Val / Test")
