import tkinter as tk
from tkinter import messagebox
import requests

# Flask server URL (running locally)
FLASK_URL = 'http://127.0.0.1:5000'

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")

        # Add Contact Frame
        self.add_contact_frame = tk.Frame(self.root)
        self.add_contact_frame.pack(pady=10)

        self.name_label = tk.Label(self.add_contact_frame, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.add_contact_frame)
        self.name_entry.grid(row=0, column=1)

        self.age_label = tk.Label(self.add_contact_frame, text="Age:")
        self.age_label.grid(row=1, column=0)
        self.age_entry = tk.Entry(self.add_contact_frame)
        self.age_entry.grid(row=1, column=1)

        self.email_label = tk.Label(self.add_contact_frame, text="Email:")
        self.email_label.grid(row=2, column=0)
        self.email_entry = tk.Entry(self.add_contact_frame)
        self.email_entry.grid(row=2, column=1)

        self.mobile_label = tk.Label(self.add_contact_frame, text="Mobile:")
        self.mobile_label.grid(row=3, column=0)
        self.mobile_entry = tk.Entry(self.add_contact_frame)
        self.mobile_entry.grid(row=3, column=1)

        self.save_button = tk.Button(self.add_contact_frame, text="Add Contact", command=self.add_contact)
        self.save_button.grid(row=4, columnspan=2)

        # View Contacts Button
        self.view_button = tk.Button(self.root, text="View Contacts", command=self.view_contacts)
        self.view_button.pack(pady=10)

        # Contact List Frame
        self.contact_list_frame = tk.Frame(self.root)
        self.contact_list_frame.pack(pady=10)

    def add_contact(self):
        # Get the data from the entry widgets
        name = self.name_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        mobile = self.mobile_entry.get()

        # Send the data to Flask to save the contact
        data = {
            'name': name,
            'age': age,
            'email': email,
            'mobile': mobile
        }

        try:
            response = requests.post(f"{FLASK_URL}/save_contact", data=data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Contact added successfully")
            else:
                messagebox.showerror("Error", "Failed to add contact")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def view_contacts(self):
        # Clear previous contact list from the frame
        for widget in self.contact_list_frame.winfo_children():
            widget.destroy()

        try:
            response = requests.get(f"{FLASK_URL}/view_contacts")
            if response.status_code == 200:
                contacts = response.json()
                row = 0
                for name, details in contacts.items():
                    contact_text = f"{name} - Age: {details['age']}, Email: {details['email']}, Mobile: {details['mobile']}"
                    contact_label = tk.Label(self.contact_list_frame, text=contact_text)
                    contact_label.grid(row=row, column=0, sticky="w")
                    row += 1
            else:
                messagebox.showerror("Error", "Failed to fetch contacts")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

# Create the Tkinter window
root = tk.Tk()
app = ContactBookApp(root)
root.mainloop()
