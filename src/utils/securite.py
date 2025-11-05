import hashlib


def hash_password(password, sel=""):
    """Hachage du mot de passe"""
    password_bytes = password.encode("utf-8") + sel.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()

def verify_password(password, hashed_password, sel=""):
    """Vérifie si le mot de passe correspond au hash"""
    return hash_password(password, sel) == hashed_password
