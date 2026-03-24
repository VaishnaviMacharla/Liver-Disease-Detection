#pyright: reportMissingImports=false
import os
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# ==============================
# PATH SETUP
# ==============================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

TEST_DIR = os.path.join(PROJECT_ROOT, "data", "final", "test")
MODEL_PATH = os.path.join(PROJECT_ROOT, "results_resnet", "best_model.keras")

IMG_SIZE = 224
BATCH_SIZE = 16

print("Test Directory:", TEST_DIR)
print("Model Path:", MODEL_PATH)

# ==============================
# CHECK PATHS
# ==============================
if not os.path.exists(TEST_DIR):
    print("❌ Test folder does not exist!")
    exit()

if not os.path.exists(MODEL_PATH):
    print("❌ Model file not found!")
    exit()

# ==============================
# LOAD MODEL
# ==============================
print("\nLoading model...")
model = tf.keras.models.load_model(MODEL_PATH)

# ==============================
# TEST DATA GENERATOR
# ==============================
test_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.resnet50.preprocess_input
)

test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

print("Number of test samples:", test_generator.samples)

if test_generator.samples == 0:
    print("❌ No test images found!")
    exit()

# ==============================
# PREDICTIONS
# ==============================
print("\nRunning predictions...")
predictions = model.predict(test_generator)

y_pred = np.argmax(predictions, axis=1)
y_true = test_generator.classes

# ==============================
# ACCURACY
# ==============================
accuracy = np.sum(y_pred == y_true) / len(y_true)
print("\n✅ Test Accuracy:", round(accuracy * 100, 2), "%")

# ==============================
# CLASSIFICATION REPORT
# ==============================
class_names = list(test_generator.class_indices.keys())

print("\n📊 Classification Report:\n")
print(classification_report(y_true, y_pred, target_names=class_names))

# ==============================
# CONFUSION MATRIX
# ==============================
cm = confusion_matrix(y_true, y_pred)

print("\n📉 Confusion Matrix (Numbers):\n")
print(cm)

# ==============================
# CONFUSION MATRIX GRAPH
# ==============================
plt.figure(figsize=(7, 6))
plt.imshow(cm, interpolation='nearest')
plt.title("Confusion Matrix")
plt.colorbar()

tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names, rotation=45)
plt.yticks(tick_marks, class_names)

# Add numbers inside boxes
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center")

plt.ylabel("Actual Label")
plt.xlabel("Predicted Label")
plt.tight_layout()

# Save the image
save_path = os.path.join(PROJECT_ROOT, "results_resnet", "confusion_matrix.png")
plt.savefig(save_path)

print("\n📁 Confusion matrix graph saved at:", save_path)

# Show graph
plt.show()

print("\n🎉 Testing Completed Successfully")