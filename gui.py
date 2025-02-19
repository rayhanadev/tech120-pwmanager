import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

import lib.db as db
import lib.generator as generator


class PasswordManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("2Cool Password Manager")

        self.master_password_var = tk.StringVar()

        master_frame = ttk.LabelFrame(master, text="Master Password")
        master_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(master_frame, text="Enter Master Password:").pack(side="left", padx=5)
        self.master_password_entry = ttk.Entry(
            master_frame, textvariable=self.master_password_var, show="*"
        )
        self.master_password_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.set_mp_button = ttk.Button(
            master_frame, text="Set", command=self.set_master_password
        )
        self.set_mp_button.pack(side="right", padx=5)

        entry_frame = ttk.LabelFrame(master, text="Manage Passwords")
        entry_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(entry_frame, text="Service:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.service_var = tk.StringVar()
        self.service_entry = ttk.Entry(entry_frame, textvariable=self.service_var)
        self.service_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Username:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(entry_frame, textvariable=self.username_var)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Password:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(entry_frame, textvariable=self.password_var)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Length (if auto-gen):").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        self.length_var = tk.IntVar(value=12)
        self.length_entry = ttk.Entry(
            entry_frame, textvariable=self.length_var, width=5
        )
        self.length_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.add_button = ttk.Button(
            entry_frame, text="Add / Update", command=self.add_entry
        )
        self.add_button.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.get_button = ttk.Button(
            entry_frame, text="Get Password", command=self.get_entry
        )
        self.get_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        list_frame = ttk.LabelFrame(master, text="Stored Services")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.list_button = ttk.Button(
            list_frame, text="List All Services", command=self.list_services
        )
        self.list_button.pack(padx=5, pady=5, anchor="w")

        self.services_text = tk.Text(list_frame, height=8, width=40)
        self.services_text.pack(padx=5, pady=5, fill="both", expand=True)

        self.db_data = None

    def set_master_password(self):
        mp = self.master_password_var.get()
        if not mp:
            messagebox.showerror("Error", "Master password cannot be empty.")
            return
        try:
            self.db_data = db.load_db(mp)
            messagebox.showinfo("Success", "Master password set. Database loaded.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load database: {e}")

    def add_entry(self):
        if self.db_data is None:
            messagebox.showerror("Error", "Please set the master password first.")
            return

        service = self.service_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        length = self.length_var.get()

        if not service or not username:
            messagebox.showerror("Error", "Service and Username are required.")
            return

        if not password:
            password = generator.generate_password(length)

        self.db_data[service] = {"username": username, "password": password}

        try:
            mp = self.master_password_var.get()
            db.save_db(self.db_data, mp)
            pyperclip.copy(password)
            messagebox.showinfo(
                "Success", f"Password for '{service}' saved and copied to clipboard."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not save entry: {e}")

    def get_entry(self):
        if self.db_data is None:
            messagebox.showerror("Error", "Please set the master password first.")
            return

        service = self.service_var.get().strip()
        if not service:
            messagebox.showerror("Error", "Please enter a service name to retrieve.")
            return

        entry = self.db_data.get(service)
        if entry:
            password = entry["password"]
            pyperclip.copy(password)
            messagebox.showinfo(
                "Password Retrieved",
                f"Username: {entry['username']}\n\nPassword copied to clipboard.",
            )
        else:
            messagebox.showwarning(
                "Not Found", f"No entry found for service: {service}"
            )

    def list_services(self):
        if self.db_data is None:
            messagebox.showerror("Error", "Please set the master password first.")
            return

        self.services_text.delete("1.0", tk.END)
        if not self.db_data:
            self.services_text.insert(tk.END, "No entries in the database.")
        else:
            self.services_text.insert(tk.END, "Stored services:\n")
            for svc in self.db_data:
                self.services_text.insert(tk.END, f" - {svc}\n")


def main():
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
