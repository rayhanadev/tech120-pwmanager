import random
import string


def generate_password(length: int = 32) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))
