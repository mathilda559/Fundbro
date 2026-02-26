import tensorflow as tf
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

model = tf.keras.applications.MobileNetV2(weights="imagenet")

def classify_image(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    decoded = decode_predictions(predictions, top=3)[0]

    # Prüfen ob Jacke oder Pullover erkannt wurde
    for pred in decoded:
        label = pred[1].lower()
        if "jacket" in label or "coat" in label:
            return "Jacke"
        if "sweatshirt" in label or "pullover" in label:
            return "Pullover"

    return "Unbekannt"
