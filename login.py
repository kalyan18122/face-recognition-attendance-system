"""
login.py
A simple Tkinter login screen. On successful login, it opens the
main dashboard (dashboard.py). Credentials are intentionally simple
since this is a small student/college project — swap in a real
username/password store if you need actual security.
"""

import tkinter as tk
from tkinter import messagebox
import dashboard

# Change these to whatever you want your login to be.
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"


def start_login():
    root = tk.Tk()
    root.title("Login - Face Attendance System")
    root.geometry("320x220")
    root.resizable(False, False)

    tk.Label(root, text="FACE ATTENDANCE SYSTEM", font=("Arial", 13, "bold")).pack(pady=15)

    form_frame = tk.Frame(root)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=8, sticky="e")
    username_entry = tk.Entry(form_frame)
    username_entry.grid(row=0, column=1, padx=5, pady=8)

    tk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=8, sticky="e")
    password_entry = tk.Entry(form_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=8)

    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            root.destroy()
            dashboard.start_dashboard()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
            password_entry.delete(0, tk.END)

    # Let pressing Enter submit the form too.
    password_entry.bind("<Return>", lambda event: attempt_login())

    tk.Button(root, text="Login", width=20, command=attempt_login).pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    start_login()
