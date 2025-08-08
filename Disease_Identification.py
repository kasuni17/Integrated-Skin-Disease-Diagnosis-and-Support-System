import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
import numpy as np
import tempfile

from recommendation import Enfeksiyonel, Ekzama, Akne, Pigment, Benign, Malign


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
        # Save to a temporary file and get its path
        with tempfile.NamedTemporaryFile(delete=False, suffix=test_image.name) as tmp_file:
            tmp_file.write(test_image.read())
            temp_file_path = tmp_file.name

    #Predict button
    if(st.button("Predict")) and test_image is not None:
        with st.spinner("Please Wait.."):
            result_index = model_prediction(temp_file_path)
            #Reading Labels
            class_name = [' Enfeksiyonel',' Ekzama',' Akne',' Pigment',' Benign',' Malign']
        
            predicted_label = class_name[result_index].strip()
            st.session_state.predicted_condition = predicted_label

        st.success("Model is Predicting it's a {}".format(class_name[result_index]))

#Recomendations 
  #Enfeksiyonel
        with st.expander("See More"):
            if result_index ==0:
                st.write('''
                             AI analysis of the uploaded skin image suggests signs consistent with the predicted condition.
                ''')
                st.image(test_image)
                st.markdown(Enfeksiyonel)

  #Ekzama
            elif(result_index==1):
                st.write('''
                             AI analysis of the uploaded skin image suggests signs consistent with the predicted condition.
                ''')
                st.image(test_image)
                st.markdown(Ekzama)

#Akne
            elif(result_index==2):
                st.write('''
                             AI analysis of the uploaded skin image suggests signs consistent with the predicted condition.
                ''')
                st.image(test_image)
                st.markdown(Akne)

#Pigment
            elif(result_index==3):
                st.write('''
                             AI analysis of the uploaded skin image suggests signs consistent with the predicted condition.
                ''')
                st.image(test_image)
                st.markdown(Pigment)

#Benign
            elif(result_index==4):
                st.write('''
                             AI analysis of the uploaded skin image suggests signs consistent with the predicted condition.
                ''')
                st.image(test_image)
                st.markdown(Benign)

#Malign
            elif(result_index==5):
                st.write('''
                             AI analysis of the uploaded skin image suggests signs consistent with the predicted condition.
                ''')
                st.image(test_image)
                st.markdown(Malign)

    

    