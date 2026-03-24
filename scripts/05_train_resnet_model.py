#pyright: reportMissingImports=false
import os
import shutil
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.utils.class_weight import compute_class_weight

# ==============================
# AUTOMATIC PROJECT ROOT PATH
# ==============================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

TRAIN_DIR = os.path.join(PROJECT_ROOT, "data", "final", "train")
VAL_DIR = os.path.join(PROJECT_ROOT, "data", "final", "val")
RESULT_DIR = os.path.join(PROJECT_ROOT, "results_resnet")

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 15

print("Train Path:", TRAIN_DIR)
print("Val Path:", VAL_DIR)

# ==============================
# OVERWRITE OLD RESULTS
# ==============================
if os.path.exists(RESULT_DIR):
    shutil.rmtree(RESULT_DIR)
os.makedirs(RESULT_DIR)

# ==============================
# DATA GENERATORS
# ==============================
train_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.resnet50.preprocess_input,
    rotation_range=10,
    zoom_range=0.1,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.resnet50.preprocess_input
)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

# ==============================
# CLASS WEIGHTS
# ==============================
classes = train_generator.classes
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(classes),
    y=classes
)
class_weights = dict(enumerate(class_weights))

print("Class Weights:", class_weights)

# ==============================
# LOAD RESNET50
# ==============================
base_model = ResNet50(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

# Freeze early layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

# ==============================
# CUSTOM CLASSIFIER HEAD
# ==============================
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)
output = Dense(3, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

# ==============================
# COMPILE MODEL
# ==============================
model.compile(
    optimizer=Adam(learning_rate=1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# ==============================
# CALLBACKS
# ==============================
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    os.path.join(RESULT_DIR, "best_model.keras"),
    monitor="val_accuracy",
    save_best_only=True
)

# ==============================
# TRAIN MODEL
# ==============================
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=[early_stop, checkpoint]
)

# ==============================
# SAVE FINAL MODEL
# ==============================
model.save(os.path.join(RESULT_DIR, "final_model.keras"))

print("\n🎉 Training Completed Successfully")