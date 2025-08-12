import streamlit as st
import sqlite3
import hashlib
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
import numpy as np
from Disease_Identification import disease_identification_page
from Learn_More import learn_more_page
from expert_panel import expert_panel_page


# Database setup
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def create_users_table():
    with sqlite3.connect('skin_disease_identification.db') as conn:
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
create_users_table()

if "logged_in_expert" not in st.session_state:
    st.session_state["logged_in_expert"] = False

# Hardcoded expert credentials (username: hashed_password)
EXPERTS = {
    "expert1": "a61a09545798dfa0f4f9a3d95e87fabbd66d49099ce0ab0c7c956097ee90238d",  # hash of "expertpass1"
    "expert2": "e74d6129f0b15bd497c8ebb6f75742b3517d72b5d39431710dc498ef144b8121",  # hash of "expertpass2"
}

def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, email, password):
    with sqlite3.connect('skin_disease_identification.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO users(username, email, password) VALUES (?, ?, ?)', 
                  (username, email, password))
        conn.commit()

def login_user(username, password):
    with sqlite3.connect('skin_disease_identification.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        data = c.fetchall()
    return data

def check_expert_login(username, password):
    hashed_password = make_hash(password)
    if username in EXPERTS and EXPERTS[username] == hashed_password:
        return True
    return False

# Model Loading
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

# Initialize app_mode in session_state if not set
if "app_mode" not in st.session_state:
    st.session_state["app_mode"] = "Home"

# Sidebar selectbox synced with session_state["app_mode"]
page_list = ["Home","Disease Identification","Learn More","DermaBot","Contact Expert","Login","Register","Expert Login","Expert Panel"]

app_mode = st.sidebar.selectbox(
    "Select Page",
    page_list,
    index=page_list.index(st.session_state["app_mode"])
)

# Update session_state app_mode if user selects a different page manually
if app_mode != st.session_state["app_mode"]:
    st.session_state["app_mode"] = app_mode


# --- Page routing ---

if st.session_state["app_mode"] == "Home":
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


elif st.session_state["app_mode"] == "Disease Identification":
    if st.session_state.get("logged_in", False):
        disease_identification_page()
    else:
        st.warning("⚠ Please log in to access Disease Identification.")

elif st.session_state["app_mode"] == "Learn More":
    learn_more_page()

elif st.session_state["app_mode"] == "Register":
    st.subheader("Create New Account")
    new_user = st.text_input("Username", key="register_username")
    new_email = st.text_input("Email", key="register_email")
    new_password = st.text_input("Password", type='password', key="register_password")

    if st.button("Register", key="register_button"):
        if new_user and new_email and new_password:
            try:
                add_user(new_user, new_email, make_hash(new_password))
                st.success("✅ Account created successfully!")
                st.info("Please go to Login page to log in.")
            except sqlite3.IntegrityError:
                st.error("❌ Username already exists.")
        else:
            st.warning("⚠ Please enter username, email, and password.")

elif st.session_state["app_mode"] == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type='password', key="login_password")

    if st.button("Login", key="login_button"):
        hashed_pass = make_hash(password)
        result = login_user(username, hashed_pass)
        if result:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"✅ Logged in as {username}")
        else:
            st.error("❌ Invalid Username or Password")

elif st.session_state["app_mode"] == "Expert Login":
    st.subheader("Expert Login")
    input_expert_username = st.text_input("Expert Username", key="input_expert_username")
    input_expert_password = st.text_input("Expert Password", type='password', key="input_expert_password")

    if st.button("Login as Expert", key="expert_login_button"):
        if check_expert_login(input_expert_username, input_expert_password):
            st.session_state["logged_in_expert"] = True
            st.session_state["expert_username"] = input_expert_username
            st.success(f"✅ Expert {input_expert_username} logged in successfully!")
        else:
            st.error("❌ Invalid Expert Username or Password")

    # Show button to enter Expert Panel after successful login
    if st.session_state.get("logged_in_expert", False):
        if st.button("Go to Expert Panel"):
            st.session_state["app_mode"] = "Expert Panel"

elif st.session_state["app_mode"] == "Expert Panel":
    if st.session_state.get("logged_in_expert", False):
        expert_panel_page()
    else:
        st.warning("⚠ Please log in as an expert to access this page.")

# Sidebar logout buttons
if st.session_state.get("logged_in", False):
    st.sidebar.markdown(f"**Logged in as:** {st.session_state['username']}")
    if st.sidebar.button("Logout", key="user_logout"):
        st.session_state.clear()
        st.session_state["app_mode"] = "Home"  # Reset to Home after logout
        st.sidebar.success("✅ Logged out successfully")

if st.session_state.get("logged_in_expert", False):
    st.sidebar.markdown(f"**Expert Logged in as:** {st.session_state['expert_username']}")
    if st.sidebar.button("Logout Expert", key="expert_logout"):
        st.session_state.pop("logged_in_expert", None)
        st.session_state.pop("expert_username", None)
        st.session_state["app_mode"] = "Home"  # Reset to Home after expert logout
        st.sidebar.success("✅ Expert logged out successfully")
