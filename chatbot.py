import streamlit as st
import requests

# ---- Your OpenRouter API Key ----
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def dermabot_page():
    st.title(" DermaBot - Your AI Assistant")

    # ---- Initialize Chat History ----
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ---- User Input ----
    user_input = st.text_input("You:", key="chat_input")

    if st.button("Send") and user_input:
        # Add user message
        st.session_state.chat_history.append(("You", user_input))

        try:
            # Call OpenRouter API
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer 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",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://www.sitename.com",  # Optional
                    "X-Title": "Streamlit ChatBot"  # Optional
                },
                json={
                    "model": "deepseek/deepseek-r1:free",
                    "messages": [{"role": "user", "content": user_input}]
                }
            )

            data = response.json()
            bot_reply = data.get("choices", [{}])[0].get("message", {}).get("content", "No reply.")

            # Add bot reply
            st.session_state.chat_history.append(("Bot", bot_reply))

        except Exception as e:
            st.session_state.chat_history.append(("Bot", f"Error: {str(e)}"))

    # ---- Display Chat History ----
    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"** You:** {msg}")
        else:
            st.markdown(f"** Bot:** {msg}")
