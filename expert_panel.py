import streamlit as st
import sqlite3

DB_NAME = "skin_disease_identification.db"  

def add_reply(query_id, reply_text):
    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO replies (query_id, expert_username, reply) 
            VALUES (?, ?, ?)
        """, (query_id, st.session_state['expert_username'], reply_text))
        c.execute("UPDATE queries SET status='answered' WHERE id=?", (query_id,))
        conn.commit()

def expert_panel_page():
    st.title(" Expert Panel")
    st.subheader(" User Queries")

    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT q.id, u.username, q.question, q.status, q.created_at
            FROM queries q
            JOIN users u ON q.user_id = u.id
            ORDER BY q.created_at DESC
        """)
        queries = c.fetchall()

    if not queries:
        st.info("No queries available yet.")
        return

    for q in queries:
        st.markdown(f"**From:** {q[1]}  \n**Question:** {q[2]}  \n {q[4]}  \n**Status:** {q[3]}")
        
        if q[3] == "pending":
            reply_text = st.text_area(f"Reply to Query {q[0]}", key=f"reply_{q[0]}")
            if st.button(f"Send Reply {q[0]}", key=f"send_{q[0]}"):
                if reply_text.strip():
                    add_reply(q[0], reply_text.strip())
                    st.success(" Reply sent!")
                else:
                    st.warning(" Please enter a reply.")
        else:
            st.info(" Already answered")
        st.markdown("---")
