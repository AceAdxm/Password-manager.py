import os
import json
from getpass import getpass
from cryptography.fernet import Fernet

# Path to store the password database
DATABASE_FILE = 'passwords.json'
KEY_FILE = 'secret.key'

# Function to generate and store encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

# Function to load the encryption key
def load_key():
    return open(KEY_FILE, 'rb').read()

# Function to encrypt data
def encrypt(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

# Function to decrypt data
def decrypt(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data.encode()).decode()

# Function to load the password database
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save the password database
def save_database(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file)

# Function to add a new account and password
def add_password(account, password, key):
    database = load_database()
    database[account] = encrypt(password, key)
    save_database(database)
    print(f"Password for {account} added successfully!")

# Function to retrieve a password
def get_password(account, key):
    database = load_database()
    if account in database:
        decrypted_password = decrypt(database[account], key)
        print(f"Password for {account}: {decrypted_password}")
    else:
        print(f"No password found for {account}!")

# Function to delete a password
def delete_password(account):
    database = load_database()
    if account in database:
        del database[account]
        save_database(database)
        print(f"Password for {account} deleted successfully!")
    else:
        print(f"No password found for {account}!")

# Function to list all accounts
def list_accounts():
    database = load_database()
    if database:
        print("Stored accounts:")
        for account in database.keys():
            print(f"- {account}")
    else:
        print("No accounts stored.")

# Main program loop
def main():
    # Generate encryption key if it doesn't exist
    if not os.path.exists(KEY_FILE):
        generate_key()

    key = load_key()

    while True:
        print("\nPassword Manager")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Delete a password")
        print("4. List all accounts")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            account = input("Enter the account name: ")
            password = getpass("Enter the password: ")
            add_password(account, password, key)
        elif choice == '2':
            account = input("Enter the account name: ")
            get_password(account, key)
        elif choice == '3':
            account = input("Enter the account name: ")
            delete_password(account)
        elif choice == '4':
            list_accounts()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()