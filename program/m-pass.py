from cryptography.fernet import Fernet
import json
import random
import string
import tkinter as tk
from tkinter import simpledialog, messagebox

# Initialize Fernet cipher suite and key
cipher_suite = None
key_file_path = 'fernet_key.txt'  # Path to store the Fernet key
original_passphrase = None  # Store the original passphrase

# Check if the cipher_suite is already initialized
def is_cipher_suite_initialized():
    return cipher_suite is not None

# Function to initialize Fernet cipher suite and key with a passphrase
def initialize_fernet(passphrase):
    global cipher_suite, original_passphrase
    if not is_cipher_suite_initialized():
        # Check if a key file exists, if so, load the key from it
        try:
            with open(key_file_path, 'rb') as key_file:
                key = key_file.read()
        except FileNotFoundError:
            # If key file doesn't exist, generate a new key
            key = Fernet.generate_key()
            with open(key_file_path, 'wb') as key_file:
                key_file.write(key)
        cipher_suite = Fernet(key)
        original_passphrase = passphrase  # Store the original passphrase
    return cipher_suite

# Function to encrypt the password
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

# Function to decrypt the password with passphrase validation
def decrypt_password(encrypted_password, passphrase):
    global original_passphrase
    if passphrase != original_passphrase:
        raise ValueError("Incorrect passphrase")
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

# Function to load passwords from JSON file
def load_passwords():
    try:
        with open('passwords.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save passwords to JSON file
def save_passwords(passwords):
    with open('passwords.json', 'w') as file:
        json.dump(passwords, file)

# Function to generate a random password
def generate_password(length=14):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Function to add a new password
def add_password():
    name = name_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not name or not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    password_length = int(password_length_entry.get())
    if password_length < 4:
        messagebox.showerror("Error", "Password length must be greater than 4 characters.")
        return

    passwords = load_passwords()

    # Check if the name is already used (must be unique)
    if name in passwords:
        messagebox.showerror("Error", f"The name '{name}' is already used. Please choose a unique name.")
        return

    # Encrypt the password using Fernet
    encrypted_password = encrypt_password(password)

    # Store the hashed password
    passwords[name] = {'username': username, 'password': encrypted_password}
    save_passwords(passwords)

    # If all checks pass, add the password
    messagebox.showinfo("Success", f"Password for {name} added successfully!")
    name_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    password_length_entry.delete(0, tk.END)
    password_length_entry.insert(0, "14")  # Reset to the default length

# Function to retrieve a password
def get_password():
    name = name_entry.get()
    passwords = load_passwords()

    if name in passwords:
        username = passwords[name]['username']
        stored_encrypted_password = passwords[name]['password']
        entered_passphrase = tk.simpledialog.askstring("Passphrase", "Enter your passphrase:")

        try:
            # Decrypt the stored encrypted password using Fernet
            decrypted_password = decrypt_password(stored_encrypted_password, entered_passphrase)
            result_text.set(f"Username: {username}\nPassword: {decrypted_password}")
        except Exception as e:
            print("Error: Decryption failed.", str(e))
            result_text.set(f"Error: {str(e)}")

    else:
        result_text.set(f"No password found for {name}.")

# Main window
root = tk.Tk()
root.title("Melken Password Manager")

# Initialize Fernet cipher suite with a passphrase
passphrase = tk.simpledialog.askstring("Passphrase", "Enter your passphrase:")
cipher_suite = initialize_fernet(passphrase)

# Labels and Entry widgets
name_label = tk.Label(root, text="Application/Website/Service")
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

password_length_label = tk.Label(root, text="Password Length:")
password_length_label.pack()
password_length_entry = tk.Entry(root)
password_length_entry.pack()
password_length_entry.insert(0, "14")  # Default length

# Buttons
add_button = tk.Button(root, text="Add Password", command=add_password)
add_button.pack()

get_button = tk.Button(root, text="Get Password", command=get_password)
get_button.pack()

generate_button = tk.Button(root, text="Generate Password", command=lambda: password_entry.insert(0, generate_password(int(password_length_entry.get()))))
generate_button.pack()

# Display result
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text)
result_label.pack()

# Start the main loop
root.mainloop()
