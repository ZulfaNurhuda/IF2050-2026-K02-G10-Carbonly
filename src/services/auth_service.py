from src.models.User import User


def verify_user(username: str, password: str) -> bool:
    user = User.find_by_username(username)
    if user is None:
        return False
    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return user.password_hash == password_hash


def get_user(username: str):
    return User.find_by_username(username)


def register_user(username: str, password: str) -> tuple[bool, str]:
    if not username or not password:
        return False, "Username and password are required"
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    success = User.create_user(username, password)
    if not success:
        return False, "Username already exists"
    return True, "User registered successfully"