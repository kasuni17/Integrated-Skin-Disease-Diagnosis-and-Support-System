import streamlit as st
import sqlite3
import os

from recommendation import Enfeksiyonel, Ekzama, Akne, Pigment, Benign, Malign

CLASS_INFO = {
    'Enfeksiyonel': Enfeksiyonel,
    'Ekzama': Ekzama,
    'Akne': Akne,
    'Pigment': Pigment,
    'Benign': Benign,
    'Malign': Malign
}
def create_records_table():
    """Create table for storing user predictions if not exists"""
    with sqlite3.connect('skin_disease_identification.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                image_name TEXT NOT NULL,
                predicted_disease TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
def add_record(user_id, image_name, predicted_disease):
    """Add a new prediction record"""
    with sqlite3.connect('skin_disease_identification.db') as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO records(user_id, image_name, predicted_disease)
            VALUES (?, ?, ?)
        ''', (user_id, image_name, predicted_disease))
        conn.commit()

def fetch_user_records(user_id):
    """Fetch all records of a user"""
    with sqlite3.connect('skin_disease_identification.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT image_name, predicted_disease, created_at
            FROM records
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        return c.fetchall()

def records_page():
    st.title(" Your Previous Predictions")

    if not st.session_state.get("logged_in", False):
        st.warning(" Please log in to view your records.")
        return

    create_records_table()

    username = st.session_state['username']
    with sqlite3.connect('skin_disease_identification.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_data = c.fetchone()
        if user_data is None:
            st.error("User not found!")
            return
        user_id = user_data[0]

    records = fetch_user_records(user_id)

    if not records:
        st.info("You have no previous predictions yet.")
        return

    for rec in records:
        image_name, predicted_disease, created_at = rec
        st.markdown(f"### Prediction on {created_at}")
        st.markdown(f"**Predicted Disease:** {predicted_disease}")
        disease_info = CLASS_INFO.get(predicted_disease, "No information available")
        st.markdown(disease_info)

        if os.path.exists(image_name):
            st.image(image_name)
        else:
            st.warning(f"Image {image_name} not found.")

        st.markdown("---")
