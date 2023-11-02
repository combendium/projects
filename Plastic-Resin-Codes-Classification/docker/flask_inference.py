#flask related imports
from flask import Flask, request, jsonify # import flask class, request module (to accept user inputs)

#import dependencies
import numpy as np
import requests
from io import BytesIO 
from PIL import Image # to open image from BytesIO object
import os # to get port number that we'll hard-code to 8080

# imports for metrics
from tensorflow.keras.metrics import Metric
import tensorflow as tf

# imports for model
from tensorflow.keras.models import load_model 
from tensorflow.keras.preprocessing import image 
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input as efficientnetv2_preprocess_input

####################

#define custum function used in training
class F1Score(Metric):
    def __init__(self, threshold=0.5, name='f1_score', **kwargs):
        super().__init__(name=name, **kwargs)
        self.threshold = threshold
        self.precision = tf.keras.metrics.Precision(threshold)
        self.recall = tf.keras.metrics.Recall(threshold)
    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = tf.cast(y_pred >= self.threshold, tf.float32)
        self.precision.update_state(y_true, y_pred, sample_weight)
        self.recall.update_state(y_true, y_pred, sample_weight)
    def result(self):
        precision = self.precision.result()
        recall = self.recall.result()
        return 2 * ((precision * recall) / (precision + recall + tf.keras.backend.epsilon()))
    def reset_state(self):
        self.precision.reset_state()
        self.recall.reset_state()
        
####################

# model url
model_url = "dropout_eff_netv2m_epoch_07_0.81_0.79.h5"

#instantiate FLASK api
api = Flask('ModelEndpoint')

#load model
def model_load():
    model = load_model(model_url, custom_objects={'F1Score': F1Score})
    return model

model= model_load()

####################

# Route 1: Health check, returns success if the API is running
@api.route('/') # this is a decorator (@api - using the Flask class' object instantiated above and creating a 'route' on this 'api' flask object. 
def home(): # just a normal Python function called 'home' with a decorator addition above
    return {"message": "Hi there!", "success": True}, 200

# Route 2: Prediction
@api.route('/predict', methods = ['POST']) 
def make_predictions(): # create a normal Python function for predictions
    try:
        user_input = request.files['image']
        
        if user_input is None:
            return jsonify({"error": "No image provided"}), 400
        image_data = user_input.read()
        image_pil = Image.open(BytesIO(image_data))
        
        # Check if the image has EXIF data and an orientation tag to reorientate for 
        exif = image_pil._getexif()
        orientation = exif.get(0x0112, 1)
        if orientation == 3:
            image_pil = image_pil.rotate(180, expand=True)
        elif orientation == 6:
            image_pil = image_pil.rotate(270, expand=True)
        elif orientation == 8:
            image_pil = image_pil.rotate(90, expand=True)
            
        #resize image
        image_pil = image_pil.resize((224, 224))
        image_array = image.img_to_array(image_pil)
        test_image = efficientnetv2_preprocess_input(image_array)
        test_image = np.expand_dims(test_image, axis=0)

        #make predictions
        predictions = model.predict(test_image)
        result = ['Recyclable' if pred[0] >0.5 else 'Non-Recyclable' for pred in predictions]
        return jsonify({'predictions': result})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


####################
# standard API run
if __name__ == '__main__': 
    api.run(host='0.0.0.0', 
            debug=True,
            port=int(os.environ.get("PORT", 8080))
           ) 