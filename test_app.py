import pytest
from index import make_hash, add_user, login_user, check_expert_login, model_prediction

# --- Test hashing ---
def test_make_hash():
    pw = "mypassword"
    hashed = make_hash(pw)
    assert hashed != pw
    assert len(hashed) == 64  

# --- Test expert login ---
def test_expert_login():
    # expert1 correct password
    assert check_expert_login("expert1", "expertpass1") is True
    # wrong password
    assert check_expert_login("expert1", "wrongpass") is False

# --- Test user add/login ---
def test_add_and_login_user():
    username = "testuser_unit"
    email = "test_unit@example.com"
    password = "secret123"
    hashed_pw = make_hash(password)

    # Add user 
    try:
        add_user(username, email, hashed_pw)
    except Exception:
        pass  

    # Login user
    result = login_user(username, hashed_pw)
    assert len(result) >= 1
    assert result[0][1] == username


def test_model_prediction(monkeypatch):
    import numpy as np
    from PIL import Image

    # Mock model
    class FakeModel:
        def predict(self, x): 
            return [[0.1, 0.9]]

    # Fake image 
    fake_image = np.zeros((224, 224, 3), dtype=np.uint8)

   
    monkeypatch.setattr("index.load_model", lambda: FakeModel())

    
    monkeypatch.setattr("tensorflow.keras.utils.load_img", lambda path, target_size: Image.fromarray(fake_image))

   
    monkeypatch.setattr("tensorflow.keras.utils.img_to_array", lambda img: np.array(img))

    # Run prediction 
    pred = model_prediction("dummy.jpg")
    assert pred == 1
