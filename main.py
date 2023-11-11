#!/usr/bin/env python3

import os, getpass, argparse, hashlib
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from secrets import choice
from dbconfig import *

## alphabets, digits, meta characters(special characters)
data = ascii_lowercase + ascii_uppercase + digits + punctuation

def generate_salt() -> bytes:
    salt = os.urandom(16)  # Generate a random 16-byte salt
    return salt

def generate_random_password(length=16) -> str:
    try:
        length = input("Enter the length of Password (default is 16): ")
        if not length or length == 'd' or length == 'default' or length == 'Default' or length == 'DEFAULT':
            length = int(16)
        elif int(length) < 4 or int(length) >= 32:
            print("Please enter length between 4 - 32 \nDefault length = 16")
            length = int(16)
        else:
            length = int(length)

        password = ''.join(choice(data) for _ in range(length))
        return password

    except ValueError:
        print("Invalid input. Please enter a valid integer for the password length.")
        return None

    except Exception as e:
        print(f"Error: {e}")

def hashed_passwd(password, salt) -> bytes:
    context = password.encode('utf-8')
    salted_password = salt + context
    sha512 = hashlib.sha512()
    sha512.update(salted_password)
    password = sha512.hexdigest()
    return password

def create_passwd(website: str, password: str, fernet_key: bytes):
    store_password(website, password, fernet_key)
    print("Password Stored Successfully!")

def show_passwd(website: str, fernet_key: bytes):
    data = retrieve_password(website, fernet_key)
    if data:
        print("Stored Password:", data)
    else:
        print("Password not found.")

def handle_create_password(username: str, fernet_key: bytes):
    create_database()
    website = input("Enter website, username, app name: ")
    if check_duplicate_password(website, fernet_key):
        print(f"Password for '{website}' already exists. Do you want to update it? (y/n/c)")
        print("Choose an option for the password:")
        print(("1. Update with Generated Password: PRESS y"))
        print(("2. NO: PRESS n"))
        print(("3. Update with Custom Password: PRESS c"))
        choice = input()
        if choice.lower() == 'y':
            password = generate_random_password()
            update_password(website, password, fernet_key)
            print(f"Generated Password: {password}")
        elif choice.lower() == 'c':
            custom_password = input("Enter your custom password: ")
            update_password(website, custom_password, fernet_key)
            print(f"Custom Password updated for '{website}'.")
        else:
            print("Password not updated.")
    else:
        print("Choose an option for the password:")
        print("1. Generate a random password")
        print("2. Use a custom password")
        choice = input()
        if choice == '1':
            generated_password = generate_random_password()
            store_password(website, generated_password, fernet_key)
            print(f"Generated Password: {generated_password}")
            print(f"Generated Password for '{website}' stored successfully.")
        elif choice == '2':
            custom_password = input("Enter your custom password: ")
            store_password(website, custom_password, fernet_key)
            print(f"Custom Password for '{website}' stored successfully.")
        else:
            print("Password not stored.")

def handle_show_password(username: str, fernet_key: bytes):
    if username:
      user_is_authenticated = login(username)
      if user_is_authenticated:
          website = input("Enter website, username, app name: ")
          show_passwd(website, fernet_key)
      else:
          print("Quiting...")

def create_user(username: str, fernet_key: bytes):
    if not username:
        username = input("Create a new username: ")
    if check_duplicate_username(username):
          print(f"User '{username}' already exists. Account creation not allowed.")
          return

    master_password = getpass.getpass("Create a MASTER password:  ")
    verify_master_password = getpass.getpass("Confirm again:  ")
    if master_password != verify_master_password:
      print("Password doesn't match")
      print("Account creation not allowed.!!!")
    else:
      salt = os.urandom(16)  # Generate a random salt
      hashed_password = hashed_passwd(master_password, salt)
      store_user_in_database(username, hashed_password, salt, fernet_key)
      print("Account created successfully.")

def verify_user(username: str, master_password: str) -> bool:
    password_hash, salt = retrieve_user_info(username)

    if password_hash is None or salt is None:
        # Handle the case where the user doesn't exist or the database is empty
        print("User not found or database is empty. Please create a user account.")
        return False

    salted_password = hashed_passwd(master_password, salt)
    return password_hash == salted_password

def login(username: str) -> bool:
    # username = input("Enter your username: ")
    master_password = getpass.getpass("Enter your MASTER password: ")

    user_is_authenticated = verify_user(username, master_password)
    if user_is_authenticated == False:
      print("Quiting...")
    return user_is_authenticated

def parse_arguments():
    parser = argparse.ArgumentParser(description="Password Management Tool")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate a random password")
    parser.add_argument("-u", "--username", metavar="username", help="Specify the username for actions")
    parser.add_argument("-cs", "--create-account", action="store_true", help="Create a new account")
    parser.add_argument("-c", "--create", action="store_true", help="Create a new password entry")
    parser.add_argument("-s", "--show", action="store_true", help="Show a stored password")
    parser.add_argument("-k", "--gen-key", "-generate-key", action="store_true", help="Generate a new Fernet key")
    parser.add_argument("-i", "--import-key", metavar="filename", help="Import a Fernet key from a file")
    parser.add_argument("-e", "--export-key", metavar="filename", help="Export the Fernet key to a file")
    parser.add_argument("-r", "--rotate-key", action="store_true", help="Rotate the encryption key")

    return parser.parse_args(), parser

def handle_arguments(args, parser, fernet_key: bytes):

    if args.create_account:
      username = args.username
      if fernet_key is None:
        fernet_key = key(username) 
      create_user(username, fernet_key)
      

    elif args.generate:
        password = generate_random_password()
        print("Generated Password:", password)

    elif args.create:
        username = args.username
        if not username:
            print("Username is required. Please provide a username.\nUse -u or --username flag to pass username.")
            return
        user_is_authenticated = login(username)
        if user_is_authenticated:
          print("User Authenticated")
          handle_create_password(username, fernet_key)

    elif args.show:
      username = args.username
      if not username:
            print("Username is required. Please provide a username.\nUse -u or --username flag to pass username.")
            return
      user_is_authenticated = login(username)
      if user_is_authenticated:
        website = input("Enter website, username, app name: ")
        show_passwd(website, fernet_key)

    elif args.gen_key:
        fernet_key = generate_new_key()
        print("Successfully Generated New Key")
        print("Please Login Again")
        print("Quiting...")

    elif args.import_key:
        filename = args.import_key
        fernet_key = import_key_from_file(filename)
        print("Key imported successfully.")
    
    
    elif args.export_key:
        filename = args.export_key
        export_key_to_file(fernet_key, filename)
        print("Key exported successfully.")
    
    elif args.rotate_key:
        rotate_key()

    else:
        parser.print_help()

# main() function:
def main():
  # Create a database file if it doesn't exist  
  create_database()  
  
  # Create key file if not exist
  fernet_key = key() 

  try:

    # export_key_to_file(fernet_key, 'key.key')
    # import_key_from_file('key.key')
    # rotate_key()
    args, parser = parse_arguments()
    handle_arguments(args, parser, fernet_key)

  except KeyboardInterrupt:
      print("\nOperation was interrupted by the user.\nQuiting...")
  except PasswordDecryptionError as e:
      print(f"Password decryption error: {e}")

if __name__ == '__main__':
    main()
