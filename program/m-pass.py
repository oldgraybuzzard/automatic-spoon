import json
import tkinter as tk
from tkinter import messagebox

def load_passwords():
    try:
        with open('passwords.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_passwords(passwords):
    with open('passwords.json', 'w') as file:
        json.dump(passwords, file)

def add_password():
    name = name_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    
    if not name or not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    passwords = load_passwords()
    passwords[name] = {'username': username, 'password': password}
    save_passwords(passwords)
    messagebox.showinfo("Success", f"Password for {name} added successfully!")
    name_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def get_password():
    name = name_entry.get()
    passwords = load_passwords()

    if name in passwords:
        username = passwords[name]['username']
        password = passwords[name]['password']
        result_text.set(f"Username: {username}\nPassword: {password}")
    else:
        result_text.set(f"No password found for {name}")

# Main window
root = tk.Tk()
root.title("Melken Password Manager")

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

# Buttons
add_button = tk.Button(root, text="Add Password", command=add_password)
add_button.pack()

get_button = tk.Button(root, text="Get Password", command=get_password)
get_button.pack()

# Display result
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text)
result_label.pack()

# Start the main loop
root.mainloop()
