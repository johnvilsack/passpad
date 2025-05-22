import tkinter as tk
from tkinter import messagebox
import random
import os
import sys

def resource_path(filename):
    """Get path to resource, whether running in dev or PyInstaller bundle."""
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

def generate_and_display():
    output_frame.delete(0, tk.END)
    for _ in range(5):
        pw = generate_password(wordlist)
        output_frame.insert(tk.END, pw)

def on_select(event):
    try:
        selected = output_frame.get(output_frame.curselection())
        copy_to_clipboard(selected)
        messagebox.showinfo("Copied", f"Password copied to clipboard:\n{selected}")
    except:
        pass

# GUI setup
root = tk.Tk()
root.title("Diceware Password Generator")
root.geometry("500x300")

tk.Label(root, text="Click to generate secure passwords:").pack(pady=10)
tk.Button(root, text="Generate Passwords", command=generate_and_display).pack(pady=5)

output_frame = tk.Listbox(root, font=("Courier", 12), height=6)
output_frame.pack(pady=10, fill=tk.BOTH, expand=True)
output_frame.bind('<<ListboxSelect>>', on_select)

# Load wordlist
wordlist = load_wordlist("eff_short_wordlist_1.txt")

root.mainloop()