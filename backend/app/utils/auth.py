import secrets

# Usuarios de prueba
fake_users = {
    "admin": "1234",
    "user": "abcd"
}

def authenticate_user(username: str, password: str) -> bool:
    return username in fake_users and fake_users[username] == password

def create_token(username: str) -> str:
    return secrets.token_hex(16)
