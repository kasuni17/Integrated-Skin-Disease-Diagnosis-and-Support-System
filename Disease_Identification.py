import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
import numpy as np
import tempfile
import sqlite3
import os

from recommendation import Enfeksiyonel, Ekzama, Akne, Pigment, Benign, Malign
from records_page import add_record  # import the function to save records

# Cache model loading for performance
@st.cache_resource()
def load_model():
    model = tf.keras.models.load_model("Trained_Skin_Disease_model.keras", compile=False)
    return model

def model_prediction(test_image_path):
    model = load_model()
    img = tf.keras.utils.load_img(test_image_path, target_size=(224, 224))
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    prediction = model.predict(x)
    return np.argmax(prediction)

def disease_identification_page():
    st.title("🦠 Disease Identification")
    st.markdown("Upload an image of the skin condition to get an AI-powered prediction.")

    test_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if test_image is not None:
        # Save uploaded image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(test_image.name)[1]) as tmp_file:
            tmp_file.write(test_image.read())
            temp_file_path = tmp_file.name

        # Predict button
        if st.button("Predict"):
            with st.spinner("Please wait while the AI analyzes the image..."):
                result_index = model_prediction(temp_file_path)
                class_name = ['Enfeksiyonel','Ekzama','Akne','Pigment','Benign','Malign']
                predicted_label = class_name[result_index].strip()
                st.session_state.predicted_condition = predicted_label

                st.success(f"✅ Model Prediction: {predicted_label}")

                # --- Save record for logged-in users ---
                if st.session_state.get("logged_in", False):
                    username = st.session_state['username']
                    with sqlite3.connect('skin_disease_identification.db') as conn:
                        c = conn.cursor()
                        c.execute("SELECT id FROM users WHERE username = ?", (username,))
                        user_data = c.fetchone()
                        if user_data:
                            user_id = user_data[0]
                            add_record(user_id, temp_file_path, predicted_label)

                # --- Display recommendations ---
                with st.expander("See Detailed Information"):
                    st.write("AI analysis suggests signs consistent with the predicted condition.")
                    st.image(test_image)

                    if result_index == 0:
                        st.markdown(Enfeksiyonel)
                    elif result_index == 1:
                        st.markdown(Ekzama)
                    elif result_index == 2:
                        st.markdown(Akne)
                    elif result_index == 3:
                        st.markdown(Pigment)
                    elif result_index == 4:
                        st.markdown(Benign)
                    elif result_index == 5:
                        st.markdown(Malign)
