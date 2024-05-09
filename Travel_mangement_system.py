import tkinter as tk
from tkinter import messagebox
import csv
import json
import datetime

class TripManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trip Management System")

        # Initialize trip fields
        self.trip_name_entry = self.create_entry("Trip detail:", 0, 0)
        self.start_date_entry = self.create_entry("Date of start (YYYY-MM-DD):", 1, 0)
        self.duration_entry = self.create_entry("Duration (days):", 2, 0)
        self.contact_info_entry = self.create_entry("Contact Info:", 3, 0)
        self.coordinator_entry = self.create_entry("Coordinator:", 4, 0)


        # Initialize traveller fields
        self.traveller_name_entry = self.create_entry("Traveller Name:", 5, 0)
        self.address_entry = self.create_entry("Address:", 6, 0)
        self.dob_entry = self.create_entry("DOB (YYYY-MM-DD):", 7, 0)
        self.emergency_contact_entry = self.create_entry("Emergency Contact:", 8, 0)
        self.gov_id_entry = self.create_entry("ID No:", 9, 0)

        # Create buttons with custom styling
        self.create_trip_button = tk.Button(root, text="Create Trip", command=self.create_trip, bg="blue", fg="white",
                                            font=("Arial", 12, "bold"))
        self.create_trip_button.grid(row=10, column=0, pady=10, padx=5, sticky="ew")
        self.create_traveller_button = tk.Button(root, text="Create Traveller", command=self.create_traveller,
                                                 bg="green", fg="white", font=("Arial", 12, "bold"))
        self.create_traveller_button.grid(row=10, column=1, pady=10, padx=5, sticky="ew")
        self.delete_trip_button = tk.Button(root, text="Delete", command=self.delete_trip, bg="red", fg="white",
                                            font=("Arial", 12, "bold"))
        self.delete_trip_button.grid(row=10, column=2, pady=10, padx=5, sticky="ew")
        self.edit_trip_button = tk.Button(root, text="Edit", command=self.edit_trip, bg="orange", fg="white",
                                          font=("Arial", 12, "bold"))
        self.edit_trip_button.grid(row=10, column=3, pady=10, padx=5, sticky="ew")
        self.close_button = tk.Button(root, text="Close", command=root.quit, bg="grey", fg="white",
                                      font=("Arial", 12, "bold"))
        self.close_button.grid(row=10, column=4, pady=10, padx=5, sticky="ew")

        # Create listboxes with custom styling
        self.trip_listbox = tk.Listbox(root, width=100, font=("Arial", 12), bg="lightgrey", selectbackground="blue")
        self.trip_listbox.grid(row=11, column=0, columnspan=5, padx=10, pady=10, sticky="ew")
        self.traveller_listbox = tk.Listbox(root, width=100, font=("Arial", 12), bg="lightgrey",
                                            selectbackground="green")
        self.traveller_listbox.grid(row=12, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

    def create_entry(self, label_text, row, column):
        tk.Label(self.root, text=label_text, font=("Arial", 12)).grid(row=row, column=column, sticky="e")
        entry = tk.Entry(self.root, font=("Arial", 12))
        entry.grid(row=row, column=column + 1)
        return entry

    def create_trip(self):
        if not self.validate_trip_fields():
            self.show_error_message("Invalid trip details. Please check and try again.")
            return

        trip_details = self.get_entry_values([
            self.trip_name_entry,
            self.start_date_entry,
            self.duration_entry,
            self.contact_info_entry,
            self.coordinator_entry
        ])
        self.trip_listbox.insert(tk.END, trip_details)
        self.write_to_csv('trips.csv', trip_details)

    def create_traveller(self):
        if not self.validate_traveller_fields():
            self.show_error_message("Invalid traveller details. Please check and try again.")
            return

        traveller_details = self.get_entry_values([
            self.traveller_name_entry,
            self.address_entry,
            self.dob_entry,
            self.emergency_contact_entry,
            self.gov_id_entry
        ])
        self.traveller_listbox.insert(tk.END, traveller_details)
        self.write_to_json('travellers.json', traveller_details)

    def delete_trip(self):
        # Clear all entries in trip and traveller fields
        self.clear_entries()
        self.show_error_message("All entries have been cleared.")

    def edit_trip(self):
        # Clear all entries in trip and traveller fields
        self.clear_entries()
        self.show_error_message("All entries have been edited.")

    def get_entry_values(self, entry_widgets):
        values = [entry.get() for entry in entry_widgets]
        return ", ".join(values)

    def validate_trip_fields(self):
        # Validation for duration
        try:
            int(self.duration_entry.get())
        except ValueError:
            self.show_error_message("Duration is a number.")
            return False

        # Validation for contact info
        contact_info = self.contact_info_entry.get()
        if len(contact_info)!= 10 or not contact_info.isdigit():
            self.show_error_message("Contact Info is a 10-digit number.")
            return False

        # Validation for date of start
        try:
            datetime.datetime.strptime(self.start_date_entry.get(), '%Y-%m-%d')
        except ValueError:
            self.show_error_message("Date of Start is a valid datetime.")
            return False

        # Additional validation logic can be added for other fields
        return True

    def validate_traveller_fields(self):
        # Validation for dob
        dob_value = self.dob_entry.get()
        try:
            datetime.datetime.strptime(dob_value, '%Y-%m-%d')
        except ValueError:
            self.show_error_message("DOB is a valid datetime.")
            return False

        # Validation for emergency contact
        emergency_contact = self.emergency_contact_entry.get()
        if len(emergency_contact)!= 10 or not emergency_contact.isdigit():
            self.show_error_message("Emergency Contact is a 10-digit number.")
            return False

        # Validation for ID No, allowing both 10-digit and 12-digit strings
        gov_id = self.gov_id_entry.get()
        if not (len(gov_id) == 10 or len(gov_id) == 12) or not gov_id.isdigit():
            self.show_error_message("ID No is a 10-digit or 12-digit string.")
            return False

        # Additional validation logic can be added for other fields
        return True

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def write_to_csv(self, filename, data):
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data.split(", "))

    def delete_from_csv(self, filename, index):
        rows = []
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                rows.append(row)
        del rows[index]
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

    def write_to_json(self, filename, data):
        data_list = data.split(", ")
        data_dict = {}
        for item in data_list:
            key, value = item.split(": ")
            data_dict[key] = value
        with open(filename, 'a') as jsonfile:
            json.dump(data_dict, jsonfile, indent=4)

    def delete_from_json(self, filename, index):
        with open(filename, 'r') as jsonfile:
            data = json.load(jsonfile)
        data_list = list(data)
        del data_list[index]
        with open(filename, 'w') as jsonfile:
            json.dump({key: data[key] for key in data_list}, jsonfile, indent=4)

    def clear_entries(self):
        # Clear trip fields
        self.trip_name_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.contact_info_entry.delete(0, tk.END)
        self.coordinator_entry.delete(0, tk.END)
        # Clear traveller fields
        self.traveller_name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.emergency_contact_entry.delete(0, tk.END)
        self.gov_id_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TripManagementApp(root)
    root.mainloop()
