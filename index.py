import streamlit as st
import sqlite3
import hashlib
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
import numpy as np
from Disease_Identification import disease_identification_page
from Learn_More import learn_more_page

# Database setup
def create_users_table():
    conn = sqlite3.connect('skin_disease_identification.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, email, password):
    conn = sqlite3.connect('skin_disease_identification.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, email, password) VALUES (?, ?, ?)', 
              (username, email, password))
    conn.commit()
    conn.close()



def login_user(username, password):
    conn = sqlite3.connect('skin_disease_identification.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

#Model Loading

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
app_mode = st.sidebar.selectbox("Select Page",["Home","Disease Identification","Learn More","DermaBot","Contact Expert","Login","Register"])


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
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        disease_identification_page()
    else:
        st.warning("⚠ Please log in to access Disease Identification.")

elif app_mode == "Learn More":
    learn_more_page()

elif app_mode == "Register":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type='password')

    if st.button("Register"):
        if new_user and new_email and new_password:
            try:
                add_user(new_user, new_email, make_hash(new_password))
                st.success("✅ Account created successfully!")
                st.info("Please go to Login page to log in.")
            except sqlite3.IntegrityError:
                st.error("❌ Username already exists.")
        else:
            st.warning("⚠ Please enter username, email, and password.")

elif app_mode == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        hashed_pass = make_hash(password)
        result = login_user(username, hashed_pass)
        if result:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"✅ Logged in as {username}")
        else:
            st.error("❌ Invalid Username or Password")

# If logged in, show extra features
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    st.sidebar.markdown(f"**Logged in as:** {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.sidebar.success("✅ Logged out successfully")
