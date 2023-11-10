from cryptography.fernet import Fernet, InvalidToken
import sqlite3
import os
import logging

# Set up the logging configuration
log_filename = 'debug.log'
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(levelname)s - %(message)s')

# database name and key path
db = 'database.db'

def debug(msg: str):
    logging.debug(msg)
    # print("[DEBUG] " + msg)

### Key ###

class PasswordDecryptionError(Exception):
    pass

def key() -> bytes:
    # Retrieve the Fernet key from the 'secret' table
    debug("Getting Fernet key from the 'secret' table.")
    fernet_key = get_key_from_database()


    if fernet_key:
        # If the key already exists in the database, return it
        debug("Fernet key retrieved successfully.")
        return fernet_key
    else:
        # If the key doesn't exist, generate a new one
        debug("Fernet key not found. Generating a new one.")
        new_key = Fernet.generate_key()
        # Store the new key in the 'secret' table
        fernet_key = store_key_in_database(new_key)
        debug("New Fernet key generated and stored.")
        return fernet_key

def generate_new_key() -> bytes:
    debug("Generating a new Fernet key.")
    new_key = Fernet.generate_key()
    fernet_key = store_key_in_database(new_key)
    debug("New Fernet key generated and stored.")
    return fernet_key

def export_key_to_file(fernet_key: bytes, filename: bytes):
    debug(f"Exporting the Fernet key to the file: {filename}")
    with open(filename, "wb") as key_file:
        key_file.write(fernet_key)

def import_key_from_file(filename: bytes) -> bytes:
    debug(f"Importing the Fernet key from the file: {filename}")
    with open(filename, "rb") as key_file:
        fernet_key = key_file.read()

    # Store the imported key in the 'secret' table
    store_key_in_database(fernet_key)

    return fernet_key

def store_key_in_database(fernet_key: bytes):
    debug(f"Storing user in the database")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Insert or update the Fernet key in the 'secret' table
    cursor.execute("INSERT OR REPLACE INTO secret (key_name, key_value) VALUES (?, ?)", ("fernet_key", fernet_key.decode()))

    conn.commit()
    conn.close()

def get_key_from_database() -> bytes or None:
    debug("Getting the Fernet key from the 'secret' table.")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Query the 'secret' table to retrieve the Fernet key
    cursor.execute("SELECT key_value FROM secret WHERE key_name = ?", ("fernet_key",))
    result = cursor.fetchone()

    conn.close()

    if result:
        key_value = result[0]
        fernet_key = key_value.encode() # Fernet(key_value.encode())
        return fernet_key
    else:
        debug("Fernet key not found in the database.")
        return None

def rotate_key():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Generate a new encryption key
    new_key = Fernet.generate_key()

    # Load the old key from the 'secret' table
    old_key = get_key_from_database()

    if old_key:
        # Retrieve and re-encrypt existing data with the new key
        reencrypt_existing_data(old_key, new_key)

        # Update the 'secret' table with the new key
        store_key_in_database(new_key)

        # Securely store the old key for potential decryption
        securely_store_old_key(old_key)

        print("Key rotation complete.")
    else:
        print("Old key not found in the 'secret' table. Key rotation aborted.")
    conn.commit()
    conn.close()

def securely_store_old_key(old_key: bytes):
    # Define a function to securely store the old key (e.g., in a backup file)
    with open("old_key.key", "wb") as key_file:
        key_file.write(old_key)

def reencrypt_existing_data(old_key: bytes, new_key: bytes):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # Define a function to re-encrypt existing data with the new key
    # Implement the logic to retrieve and re-encrypt existing data
    # This may involve querying the 'passwords' table and re-encrypting each password
    # using the old key for decryption and the new key for encryption

    # Example: Loop through existing data and re-encrypt
    # for each record in the 'passwords' table
    cursor.execute("SELECT id, encrypted_password FROM passwords")
    for row in cursor.fetchall():
        encrypted_password = row[1]
        fernet_old = Fernet(old_key)
        decrypted_password = fernet_old.decrypt(encrypted_password)
        fernet_new = Fernet(new_key)
        reencrypted_password = fernet_new.encrypt(decrypted_password)

        # Update the record with the re-encrypted password
        cursor.execute("UPDATE passwords SET encrypted_password = ? WHERE id = ?", (reencrypted_password, row[0]))  
    conn.commit()
    conn.close()

### Database ###

def create_database():
    debug("Creating the database if it doesn't exist.")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Create the 'users' table with columns 'username', 'password_hash', and 'salt'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT,
            salt BLOB
        )
    ''')

    # Create a table to store encrypted passwords
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, website TEXT, encrypted_password TEXT)''')


    # Create the 'secret' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS secret (
            key_name TEXT PRIMARY KEY,
            key_value TEXT
        )
    ''')

    conn.commit()
    conn.close()

def check_duplicate_username(username: str):
    debug(f"Checking for duplicate username: {username}")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    conn.close()

    if existing_user:
        debug(f"Found duplicate username: {username}")
    else:
        debug(f"Username {username} is not a duplicate.")

    return existing_user is not None

def store_user_in_database(username: str, hashed_password: bytes, salt: bytes):
    debug(f"Storing user in the database: {username}")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Assuming you have a table named 'users' with columns 'username', 'password_hash', and 'salt'
    cursor.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)", (username, hashed_password, salt))

    conn.commit()
    conn.close()

def retrieve_user_info(username: str):
    debug(f"Retrieving user info for username: {username}")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Assuming you have a table named 'users' with columns 'username', 'password_hash', and 'salt'
    cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        password_hash, salt = result
        debug("User info retrieved successfully.")
        return password_hash, salt
    else:
        debug("User info not found.")
        return None, None

### Passwords ###

def check_duplicate_password(website: str, fernet_key: bytes):
    existing_password = retrieve_password(website, fernet_key)
    return existing_password is not None

def retrieve_password(website: str, fernet_key: bytes) -> str or None:
    debug(f"Retrieving password for website: {website}")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT encrypted_password FROM passwords WHERE website=?", (website,))
    result = cursor.fetchone()

    if not result:
        debug(f"Password not found for website: {website}")
        return None

    try:
        password = decrypt_password(result[0], fernet_key)
        debug("Password retrieved and decrypted successfully.")
        return password

    except InvalidToken:
        debug("Failed to decrypt the password. Keys may not match.")
        raise PasswordDecryptionError("Failed to decrypt the password. Keys may not match.")

    conn.close()

    return None

def store_password(website: str, password: str, fernet_key: str):
    debug(f"Fernet key in store_passwd func before encrypt_password() func")
    debug(f"Storing password for website: {website}")
    encrypted_password = encrypt_password(password, fernet_key)
    debug(f"Fernet key after encrypt_passwd func which return and store in encrypted_password")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO passwords (website, encrypted_password) VALUES (?, ?)",
                   (website, encrypted_password))
    conn.commit()
    conn.close()

def update_password(website: str, new_password: str, fernet_key: bytes):
  debug(f"Updating password for website: {website}")

  if check_duplicate_password(website, fernet_key):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Retrieve the existing password
    existing_password = retrieve_password(website, fernet_key)
    print(f"Existing Password for '{website}': {existing_password}")

    # Replace the existing password with the new one using an SQL UPDATE statement
    cursor.execute("UPDATE passwords SET encrypted_password = ? WHERE website = ?", (encrypt_password(new_password, fernet_key), website))
    conn.commit()
    conn.close()

    print(f"Updated Password for '{website}': {new_password}")

  else:
    # Password doesn't exist, create a new password
    store_password(website, new_password, fernet_key)
    print(f"Generated Password for '{website}': {new_password}")
    print(f"Password for '{website}' stored successfully.")

def encrypt_password(password: str, fernet_key: bytes):
    debug(f"Encrypting the password. {fernet_key}")
    fernet = Fernet(fernet_key)
    debug(f"Fernet key after return Fernet() func and store in fernet")
    encrypted_password = fernet.encrypt(password.encode())
    debug(f"Fernet key after encryption done on passwd and return encrypted_password ")
    return encrypted_password

def decrypt_password(encrypted_password: str, fernet_key: bytes):
    debug("Decrypting the password.")
    fernet = Fernet(fernet_key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# debug.log file close
logging.shutdown()
