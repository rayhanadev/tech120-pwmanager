import os
import json
from lib.encryption import derive_key, encrypt_data, decrypt_data

DB_FILE = "passwords.dat"
SALT_FILE = "salt.salt"


def get_salt() -> bytes:
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    else:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    return salt


def load_db(master_password: str) -> dict:
    salt = get_salt()
    key = derive_key(master_password, salt)
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "rb") as f:
        encrypted_data = f.read()
    try:
        decrypted_data = decrypt_data(encrypted_data, key)
        data = json.loads(decrypted_data.decode("utf-8"))
    except Exception as e:
        print("Error decrypting database. Perhaps the master password is incorrect.")
        raise e
    return data


def save_db(data: dict, master_password: str):
    salt = get_salt()
    key = derive_key(master_password, salt)
    serialized_data = json.dumps(data).encode("utf-8")
    encrypted_data = encrypt_data(serialized_data, key)
    with open(DB_FILE, "wb") as f:
        f.write(encrypted_data)
