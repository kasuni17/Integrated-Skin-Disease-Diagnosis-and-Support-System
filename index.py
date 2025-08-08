import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
import numpy as np
from Disease_Identification import disease_identification_page
from Learn_More import learn_more_page


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

#Sidebar
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page",["Home","Disease Identification","Learn More","DermaBot","Contact Expert","Login"])


if app_mode == "Home":
    # image_path = "home_banner.jpg"
    # st.image(image_path, use_column_width=True)
    st.markdown("""
    ## **AI-Based Skin Disease Identification and Support System**

#### **Welcome to the Intelligent Dermatology Assistant**

Our platform offers an innovative, AI-powered solution for analyzing and identifying potential skin conditions from medical images. Designed for both healthcare professionals and the general public, this tool combines advanced machine learning technology with medical knowledge to assist in early detection and support.

With just an image, our intelligent system can provide predictions and educational support — improving awareness, encouraging timely action, and reducing dependency on in-person evaluations in remote areas.

---

#### **Why Use AI for Skin Health?**

Skin-related health issues are common and often underdiagnosed, especially in underserved regions. Our platform empowers users with:
- Fast, automated screening
- User-friendly interface
- Educational insights to better understand potential conditions

By integrating AI into dermatological analysis, we offer a reliable support system to assist early detection and reduce the burden on medical professionals.

---

#### **Key Features of the Platform**

- ✅ **Automated Image Prediction**  
  Upload images and receive AI-generated analysis instantly.

- 🧠 **Advanced Deep Learning Model**  
  Built using cutting-edge neural networks trained on thousands of expert-labeled skin images.

- 🔍 **Interactive Visual Feedback**  
  Results are accompanied by visual cues and probabilities to increase understanding.

- 📘 **Support and Resources**  
  Learn about causes, symptoms, and general care tips to guide your next steps.

- 🔐 **Secure and Confidential**  
  Your data remains private. No images are stored or shared.

---

#### **How It Works**

1. **Capture or Upload**: Upload a clear image of the affected skin area.
2. **Analyze**: The AI model processes the image and predicts the most likely condition.
3. **Understand**: Review detailed insights and suggestions to guide your awareness or next action.

---

#### **Get Started Today**

- 📤 **Upload Your Image** to begin an instant analysis.
- 📊 **View Results and Insights** to learn more about your skin health.
- 📚 **Explore Support Resources** for education and next steps.

---

#### **Need Help?**

Have questions or want to collaborate with us? [Contact our team](#) to find out how this platform can support your health or organization.

    """)

elif app_mode == "Disease Identification":
    disease_identification_page()

elif app_mode == "Learn More":
        learn_more_page()
