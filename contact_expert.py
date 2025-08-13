import streamlit as st
import sqlite3

def get_user_id(username):
    with sqlite3.connect('skin_disease_identification.db') as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        return c.fetchone()[0]

def contact_expert_page():
    st.subheader("💬 Contact Expert")
    question = st.text_area("Enter your question for the expert")

    if st.button("Send Message"):
        if question.strip():
            with sqlite3.connect('skin_disease_identification.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO queries (user_id, question) VALUES (?, ?)",
                          (get_user_id(st.session_state['username']), question))
                conn.commit()
            st.success("✅ Message sent to expert!")
        else:
            st.warning("⚠ Please enter a question.")

    st.markdown("### 📬 Your Queries & Replies")
    with sqlite3.connect('skin_disease_identification.db') as conn:
        c = conn.cursor()
        c.execute("""SELECT q.id, q.question, q.status, r.reply, r.created_at 
                     FROM queries q
                     LEFT JOIN replies r ON q.id = r.query_id
                     WHERE q.user_id = ?
                     ORDER BY q.created_at DESC""",
                  (get_user_id(st.session_state['username']),))
        rows = c.fetchall()

    for row in rows:
        st.markdown(f"**Question:** {row[1]} *(Status: {row[2]})*")
        if row[3]:
            st.success(f"**Reply:** {row[3]} (📅 {row[4]})")
        else:
            st.info("⏳ Waiting for reply...")
        st.markdown("---")
