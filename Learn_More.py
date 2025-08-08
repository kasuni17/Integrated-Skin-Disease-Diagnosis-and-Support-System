import streamlit as st

def learn_more_page():
    st.title("🦠 Learn More About Your Skin Condition")

    if "predicted_condition" in st.session_state:
        condition = st.session_state.predicted_condition
        st.subheader(f"📌 Condition: **{condition}**")

        st.write("Based on your uploaded skin image, we have provided an educational video to help you understand this condition better.")

        tutorial_videos = {
            "Enfeksiyonel": "https://www.youtube.com/embed/xbEqpYTkuXg?si=HHiTHyZ8geEv8xRG",
            "Ekzama": "https://www.youtube.com/embed/EY2sP_oOH3I",
            "Akne": "https://youtu.be/xbEqpYTkuXg?si=Ot6aH54hlXX7YvHs",
            "Pigment": "https://www.youtube.com/embed/6KqUyvAVzjY",
            "Benign": "https://www.youtube.com/embed/IRK4pvTYIrw",
            "Malign": "https://www.youtube.com/embed/dFCGzKo77vQ",
        }

        if condition in tutorial_videos:
            st.video(tutorial_videos[condition])
        else:
            st.warning("No tutorial video available for this condition yet.")
    else:
        st.error("No skin condition predicted yet. Please predict from the Disease Identification page first.")
