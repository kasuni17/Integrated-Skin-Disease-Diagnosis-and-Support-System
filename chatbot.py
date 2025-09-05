import streamlit as st
import requests


API_KEY = "API KEY"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def dermabot_page():
    st.title("DermaBot - Your AI Assistant")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    user_input = st.text_input("You:", key="chat_input")

    if st.button("Send") and user_input:
        st.session_state.chat_history.append(("You", user_input))

        try:
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer API KEY",
                    "Content-Type": "application/json",
                    "X-Title": "Streamlit ChatBot" 
                },
                json={
                    "model": "deepseek/deepseek-r1-distill-llama-70b:free",
                    "messages": [{"role": "user", "content": user_input}]
                }
            )

            data = response.json()
   
            if "choices" in data and len(data["choices"]) > 0:
                bot_reply = data["choices"][0]["message"]["content"]
            else:
                bot_reply = "No reply from model."

            st.session_state.chat_history.append(("Bot", bot_reply))

        except Exception as e:
            st.session_state.chat_history.append(("Bot", f"Error: {str(e)}"))

   
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Bot:** {msg}")
