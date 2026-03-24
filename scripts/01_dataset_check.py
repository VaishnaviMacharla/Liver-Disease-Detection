import os
import pandas as pd

# BASE PATHS
BASE_DIR = "../data/raw/Project_last"
LABELS_DIR = os.path.join(BASE_DIR, "Labels")
CSV_PATH = os.path.join(BASE_DIR, "dataset.csv")

classes = ["Grade_1", "Grade_2", "Healthy"]

def check_dataset():
    print("🔍 Checking dataset structure...\n")

    # Check CSV file
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        print(f"✅ CSV loaded successfully. Shape: {df.shape}")
    else:
        print("❌ dataset.csv not found")
        return

    # Check folders
    for cls in classes:
        print(f"\n📂 Class: {cls}")

        img_dir = os.path.join(LABELS_DIR, cls, "image")
        seg_dir = os.path.join(LABELS_DIR, cls, "segmentation")

        if not os.path.exists(img_dir):
            print("❌ image folder missing")
            continue

        if not os.path.exists(seg_dir):
            print("❌ segmentation folder missing")
            continue

        print("  Images count:", len(os.listdir(img_dir)))
        print("  Segmentation subfolders:", os.listdir(seg_dir))

        if cls == "Healthy" and "mass" in os.listdir(seg_dir):
            print("⚠️ ERROR: Healthy should not have a mass folder")

    print("\n✅ Dataset verification completed.")

if __name__ == "__main__":
    check_dataset()
