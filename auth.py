def login(users, username, password):
    return bool(username) and users.get(username) == password

def register(users, username, password, confirm):
    username = username.strip()
    if not username or not password:
        return "Enter both username and password."
    if username in users:
        return "That username already exists."
    if len(password) < 6:
        return "Password must contain at least 6 characters."
    if password != confirm:
        return "Passwords do not match."
    users[username] = password
    return "ok"
