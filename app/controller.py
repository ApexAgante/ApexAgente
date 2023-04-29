def check_user(user: str, password: str):
    if not user:
        return None
    if user.strip() == 'admin':
        if password == '12345':
            return 'Administrator'
        else:
            return None
    return user.capitalize()
