import tkinter as tk
from tkinter import messagebox
import random
import os
import sys

def resource_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def load_wordlist(filename):
    wordlist = {}
    try:
        with open(resource_path(filename), 'r') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    key, word = parts
                    wordlist[key] = word
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load word list:\n{e}")
    return wordlist

def roll_die():
    return str(random.randint(1, 6))

def roll_4_digits():
    return ''.join(roll_die() for _ in range(4))

def get_word(wordlist):
    for _ in range(20):
        roll = roll_4_digits()
        if roll in wordlist:
            return wordlist[roll]
    return 'oops'

def generate_password(wordlist):
    words = [get_word(wordlist) for _ in range(4)]
    words[0] = words[0].capitalize()
    number = str(random.randint(10, 99))
    special = random.choice('!@#$%^&*?')
    return f"{'-'.join(words)}-{number}{special}"

def copy_to_clipboard(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

def highlight_only(confirm_label, password):
    confirm_label.config(text="Copied!", fg="white")
    root.after(1000, lambda: confirm_label.config(text=""))
    editable_entry.delete(0, tk.END)
    editable_entry.insert(0, password)

def generate_and_display():
    for widget in output_frame.winfo_children():
        widget.destroy()

    for _ in range(5):
        pw = generate_password(wordlist)

        row = tk.Frame(output_frame)
        row.pack(pady=8)

        content = tk.Frame(row)
        content.pack()

        label = tk.Label(
            content,
            text=pw,
            font=("Courier", 16),
            anchor="w",
            padx=10,
            pady=4,
            width=30
        )
        label.pack(side=tk.LEFT)

        copy_icon = tk.Label(
            content,
            text="📋",
            font=("Arial", 16),
            bg=root["bg"],
            cursor="hand2",
            padx=8
        )
        copy_icon.pack(side=tk.LEFT)

        confirm_label = tk.Label(
            content,
            text="",
            font=("Arial", 11),
            fg="white",
            bg=root["bg"],
            width=8,
            anchor="w"
        )
        confirm_label.pack(side=tk.LEFT)

        def make_copy_handler(pw=pw, confirm_label=confirm_label):
            def handler(event=None):
                copy_to_clipboard(pw)
                highlight_only(confirm_label, pw)
            return handler

        copy_icon.bind("<Button-1>", make_copy_handler())

def copy_modified_password():
    modified_pw = editable_entry.get()
    if modified_pw.strip():
        copy_to_clipboard(modified_pw)
        modify_feedback.config(text="Copied!", fg="green")
        root.after(1000, lambda: modify_feedback.config(text=""))

# GUI setup
root = tk.Tk()
root.title("Diceware Password Generator")
root.geometry("700x580")

tk.Label(root, text="Click to generate secure passwords:", font=("Arial", 14)).pack(pady=(15, 5))
tk.Button(root, text="Generate Passwords", font=("Arial", 12), command=generate_and_display).pack(pady=5)

output_frame = tk.Frame(root)
output_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Editable box + button
edit_frame = tk.Frame(root)
edit_frame.pack(pady=(20, 10))

tk.Label(edit_frame, text="Editable Password:", font=("Arial", 12)).pack(anchor="w")

editable_entry = tk.Entry(edit_frame, font=("Courier", 14), width=40)
editable_entry.pack(side=tk.LEFT, padx=(0, 10))

copy_mod_btn = tk.Button(edit_frame, text="Copy Modified", command=copy_modified_password)
copy_mod_btn.pack(side=tk.LEFT)

modify_feedback = tk.Label(edit_frame, text="", font=("Arial", 11), fg="green")
modify_feedback.pack(side=tk.LEFT, padx=(10, 0))

# Shared state
wordlist = load_wordlist("eff_short_wordlist_1.txt")

root.mainloop()