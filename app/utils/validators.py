import re

import re

def is_valid_username(username: str) -> bool:
    """
    Проверяет валидность имени пользователя:
    - 3–20 символов
    - только английские буквы, цифры и подчеркивания
    - обязательно хотя бы одна английская буква
    """
    if not 3 <= len(username) <= 20:
        return False
    if not re.match(r'^[A-Za-z0-9_]+$', username):
        return False
    if not re.search(r'[A-Za-z]', username):
        return False
    return True


def is_valid_password(password: str) -> bool:
    """
    Проверяет валидность пароля:
    - минимум 6 символов
    - хотя бы одна цифра
    """
    if len(password) < 6:
        return False
    if not re.search(r'\d', password):
        return False
    return True
