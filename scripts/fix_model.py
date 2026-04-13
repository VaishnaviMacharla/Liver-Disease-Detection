import os
import tensorflow as tf

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
OLD_MODEL_PATH = os.path.join(PROJECT_ROOT, "results_resnet", "best_model.keras")
NEW_MODEL_PATH = os.path.join(PROJECT_ROOT, "results_resnet", "best_model_fixed.keras")

print("Fixing Keras version compatibility...")
print(f"Old model: {OLD_MODEL_PATH}")

# Load old model (may show warnings)
model = tf.keras.models.load_model(OLD_MODEL_PATH, compile=False)

# Save with current Keras version
model.save(NEW_MODEL_PATH)
model = tf.keras.models.load_model(NEW_MODEL_PATH)  # Test reload

print(f"✅ Fixed model saved: {NEW_MODEL_PATH}")
print("Update MODEL_FILENAME = 'best_model_fixed.keras' in predict_with_gradcam.py")

