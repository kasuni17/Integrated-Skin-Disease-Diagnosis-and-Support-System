import hashlib

def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

print("expert1 password hash:", make_hash("expertpass1"))
print("expert2 password hash:", make_hash("expertpass2"))
