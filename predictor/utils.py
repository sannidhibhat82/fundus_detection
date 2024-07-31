# predictor/utils.py
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

class DiseasePredictor:
    def __init__(self):
        self.model = tf.keras.models.load_model('path/to/your/model.h5')
    
    def predict(self, image_path):
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Convert single image to a batch
        predictions = self.model.predict(img_array)
        return predictions
