#import dependencies
import streamlit as st
import numpy as np
import os # to get port number that we'll hard-code to 8080  for now

# imports for metrics
from tensorflow.keras.metrics import Metric
import tensorflow as tf

# imports for model
from tensorflow.keras.models import load_model # to load model from saved file earlier
from tensorflow.keras.preprocessing import image # to do image processing in the required format for predictions
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input as efficientnetv2_preprocess_input

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
st.set_page_config(
    page_title="♻️Recycling with Plastic Resin Code🔢",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title("♻️Classifying plastic resin codes recycling")

@st.cache_resource
#load model and metric
def model_load():
#    model_url = ' '
    model_path = 'dropout_eff_netv2m_epoch_07_0.81_0.79.h5'
#    urllib.request.urlretrieve(model_url, model_path)
    model = tf.keras.models.load_model(model_path, custom_objects={'F1Score': F1Score})
    return model
    
model=model_load()

#load image
uploaded_image = st.file_uploader(":system-color[Upload an image in the box below to begin.]", type=["jpg", "png", "jpeg"])

if uploaded_image is None:
    st.write(f'<p style="font-size:20px;">Step 1: Upload a file from a local drive or drag an image from browser</p>', unsafe_allow_html=True)
    st.write(f'<p style="font-size:20px;font-style:bold;">Step 2: Wait for result of classification</p>', unsafe_allow_html=True)
    st.write(f'<p style="font-size:16px;color:blue;font-style:bold;">Please use a picture with the symbol framed as big as possible </p>', unsafe_allow_html=True)
    st.write(f'<p style="font-size:16px;font-style:italic;">Disclaimer: Still in beta. classification is not perfect. </p>', unsafe_allow_html=True)


else:
    with st.spinner(text="In progress.. Please give it a few seconds.."):
        # Preprocess the image
        test_image = image.load_img(uploaded_image, target_size=(224, 224))
        test_image = image.img_to_array(test_image) 
        test_image = np.expand_dims(test_image, axis=0)
        test_image = efficientnetv2_preprocess_input(test_image)
    
        # Make predictions
        predictions = model.predict(test_image)
        result = ['Recyclable' if pred[0] >0.5 else 'Non-Recyclable' for pred in predictions]
        
        # Display results
        st.image(uploaded_image, 
                 caption = f'Uploaded image: {uploaded_image.name}',
                 width = 224)
#                 use_column_width=False)
        st.write(f'<p style="font-size:24px;color:blue;">Uploaded image "{uploaded_image.name}":  {result[0]} type </p>', unsafe_allow_html=True)

