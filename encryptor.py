from cryptography.fernet import Fernet
import argparse
import os

# This will be the name of the key file we save/load from
KEY_FILE = "password.key"

# Makes a new key and saves it in a file
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)

# Loads the saved key
def load_key():
    return open(KEY_FILE, 'rb').read()

# Encrypts the file and saves it as filename.enc
def encrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(file_path + ".locked", 'wb') as f:
        f.write(encrypted)

# Decrypts the file and saves it with the original filename
def decrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, 'rb') as f:
        encrypted = f.read()

    decrypted = fernet.decrypt(encrypted)

    with open(file_path.replace(".locked", ""), 'wb') as f:
        f.write(decrypted)

# Command line setup
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files")
    parser.add_argument("mode", choices=["encrypt", "decrypt", "generate-key"], help="What you want to do")
    parser.add_argument("file", nargs='?', help="The file to work on (not needed if generating a key)")

    args = parser.parse_args()

    if args.mode == "generate-key":
        generate_key()
        print("🔑 Key saved to 'password.key'")
    elif args.mode == "encrypt":
        encrypt_file(args.file)
        print(f"🔒 File encrypted: {args.file}.locked")
    elif args.mode == "decrypt":
        decrypt_file(args.file)
        print(f"🔓 File decrypted: {args.file.replace('.locked', '')}")
