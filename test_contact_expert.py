import pytest
import sqlite3
from pathlib import Path
import contact_expert

# Temporary database fixture
@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test.db"
    
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)''')
    c.execute('''CREATE TABLE queries (id INTEGER PRIMARY KEY, user_id INTEGER, question TEXT, status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE replies (id INTEGER PRIMARY KEY, query_id INTEGER, expert_username TEXT, reply TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', ("testuser", "test@test.com", "hashedpass"))
    conn.commit()
    conn.close()
    return db_file

# Test get_user_id
def test_get_user_id(monkeypatch, temp_db):
    original_connect = sqlite3.connect
    
    monkeypatch.setattr(contact_expert.sqlite3, "connect", lambda _: original_connect(temp_db))

    user_id = contact_expert.get_user_id("testuser")
    assert user_id == 1

# Test sending a question
def test_contact_expert_page_send(monkeypatch, temp_db):
    original_connect = sqlite3.connect
    monkeypatch.setattr(contact_expert.sqlite3, "connect", lambda _: original_connect(temp_db))

    
    monkeypatch.setattr(contact_expert.st, "text_area", lambda label: "What is acne?")
    monkeypatch.setattr(contact_expert.st, "button", lambda label: True)
    monkeypatch.setattr(contact_expert.st, "success", lambda msg: msg)
    monkeypatch.setattr(contact_expert.st, "warning", lambda msg: msg)
    monkeypatch.setattr(contact_expert.st, "info", lambda msg: msg)
   
    monkeypatch.setattr(contact_expert.st, "session_state", {"username": "testuser"})

    
    contact_expert.contact_expert_page()

    
    conn = sqlite3.connect(temp_db)
    c = conn.cursor()
    c.execute("SELECT question FROM queries WHERE user_id = 1")
    result = c.fetchone()[0]
    assert result == "What is acne?"
    conn.close()


def test_contact_expert_page_display(monkeypatch, temp_db):
    original_connect = sqlite3.connect
    monkeypatch.setattr(contact_expert.sqlite3, "connect", lambda _: original_connect(temp_db))

    
    conn = sqlite3.connect(temp_db)
    c = conn.cursor()
    c.execute("INSERT INTO queries (user_id, question, status) VALUES (?, ?, ?)", (1, "Test question?", "answered"))
    query_id = c.lastrowid
    c.execute("INSERT INTO replies (query_id, reply) VALUES (?, ?)", (query_id, "This is a reply"))
    conn.commit()
    conn.close()

   
    monkeypatch.setattr(contact_expert.st, "text_area", lambda label: "")
    monkeypatch.setattr(contact_expert.st, "button", lambda label: False)
    monkeypatch.setattr(contact_expert.st, "success", lambda msg: msg)
    monkeypatch.setattr(contact_expert.st, "info", lambda msg: msg)
    monkeypatch.setattr(contact_expert.st, "markdown", lambda msg: msg)
    monkeypatch.setattr(contact_expert.st, "warning", lambda msg: msg)
    monkeypatch.setattr(contact_expert.st, "session_state", {"username": "testuser"})

    contact_expert.contact_expert_page()
