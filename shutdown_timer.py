import os
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import pyotp
from datetime import datetime
import ctypes

# Shared secret for TOTP (use a base32 encoded secret)
SECRET = "JBSWY3DPEHPK3PXP"

def generate_daily_password():
    # Generate a TOTP object with the given secret
    totp = pyotp.TOTP(SECRET, interval=86400)  # 86400 seconds = 1 day
    return totp.now()

def lock_computer():
    # Use ctypes to lock the computer
    ctypes.windll.user32.LockWorkStation()

def show_warning():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showwarning("Warning", "Only 5 minutes left until lock!")
    root.destroy()

def countdown_timer(lock_time):
    total_seconds = lock_time * 60
    warning_time = 300  # 5 minutes in seconds
    
    while total_seconds > 0:
        if total_seconds == warning_time:
            show_warning()
        time.sleep(1)
        total_seconds -= 1

    lock_computer()

def main():
    # Generate today's password
    correct_password = generate_daily_password()

    # Create a fullscreen window without window decorations
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(bg='black')
    root.focus_set()
    
    # Remove the ability to close the window using Alt+F4
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # Create a label for the password prompt
    label = tk.Label(root, text="Enter Password:", font=("Arial", 24), fg="white", bg="black")
    label.pack(pady=20)
    
    # Create an entry widget for password input
    password_entry = tk.Entry(root, font=("Arial", 24), show="*", fg="black", bg="white")
    password_entry.pack(pady=20)
    password_entry.focus_set()

    def check_password(event=None):
        if password_entry.get() == correct_password:
            root.destroy()
            set_lock_timer()
        else:
            messagebox.showerror("Error", "Incorrect password. Access denied.")
    
    password_entry.bind('<Return>', check_password)
    
    # Run the Tkinter event loop
    root.mainloop()

def set_lock_timer():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    try:
        lock_time = simpledialog.askinteger("Lock Timer", "Enter time in minutes until lock:")
        if lock_time:
            messagebox.showinfo("Timer Set", f"Computer will lock in {lock_time} minute(s).")
            # Start the countdown timer in a separate thread
            countdown_thread = threading.Thread(target=countdown_timer, args=(lock_time,), daemon=True)
            countdown_thread.start()
            countdown_thread.join()  # Ensure the main script waits for the countdown to complete
        else:
            messagebox.showwarning("No Time Set", "No time was set. The computer will not lock.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number of minutes.")
    finally:
        root.destroy()

if __name__ == "__main__":
    main()
