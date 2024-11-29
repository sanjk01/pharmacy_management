import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydata"
)

def enter_prescription():
    # Collect input data
    patient_name = entry_patient_name.get()
    patient_age = entry_patient_age.get()
    doctor_name = entry_doctor_name.get()
    prescription_date = entry_date.get()

    if not patient_name or not prescription_date:
        messagebox.showerror("Error", "All fields are necessary.")
        return

    # Insert data into the prescription table
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO prescription (patient_name, patient_age, doctor_name, prescription_date) VALUES (%s, %s, %s, %s)",
        (patient_name, patient_age, doctor_name, prescription_date)
    )
    db.commit()
    messagebox.showinfo("Success", "Prescription details entered into table.")

def add_medicine():
    # Collect input data
    pres_number = entry_presc_number.get()
    med_name = entry_med_name.get()
    quantity = entry_quantity.get()
    disease = entry_disease.get()
    dosage_time = entry_dosage_time.get()

    if not pres_number or not med_name or not quantity:
        messagebox.showerror("Error", "All fields are necessary.")
        return

    # Check if prescription ID exists
    cursor = db.cursor()
    cursor.execute("SELECT * FROM prescription WHERE prescription_id = %s", (pres_number,))
    prescription = cursor.fetchone()

    if prescription:
        messagebox.showinfo("Success", "Prescription found.")
        # Insert into presc_items table
        cursor.execute(
            "INSERT INTO presc_items (prescription_id, med_name, quantity, disease, dosage_time) VALUES (%s, %s, %s, %s, %s)",
            (pres_number, med_name, quantity, disease, dosage_time)
        )
        db.commit()
        
        # Update the Treeview with new medicine entry
        med_tree.insert("", tk.END, values=(med_name, quantity, disease, dosage_time))
        
        # Clear prescription items fields
        entry_presc_number.delete(0, tk.END)
        entry_med_name.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_disease.delete(0, tk.END)
        entry_dosage_time.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Prescription ID not found.")

def clear_prescription_fields():
    # Clear all fields in the prescription frame
    entry_patient_name.delete(0, tk.END)
    entry_patient_age.delete(0, tk.END)
    entry_doctor_name.delete(0, tk.END)
    entry_date.delete(0, tk.END)

# Main application window
root = tk.Tk()
root.title("Prescription Information")
root.geometry("850x700")
root.configure(bg="#f8f9fa")

# Header
header = tk.Label(root, text="Prescription Information", font=("Helvetica", 18, "bold"), bg="#4caf50", fg="white")
header.pack(fill="x", pady=(10, 20))

# Top Frame for basic prescription details
top_frame = tk.Frame(root, bg="#e0f7fa", bd=2, relief="solid", padx=20, pady=10)
top_frame.pack(fill="x", padx=20, pady=10)

tk.Label(top_frame, text="Patient Name:", bg="#e0f7fa").grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_patient_name = tk.Entry(top_frame, width=20)
entry_patient_name.grid(row=0, column=1, pady=5)

tk.Label(top_frame, text="Patient Age:", bg="#e0f7fa").grid(row=0, column=2, sticky="w", padx=10, pady=5)
entry_patient_age = tk.Entry(top_frame, width=10)
entry_patient_age.grid(row=0, column=3, pady=5)

tk.Label(top_frame, text="Doctor Name:", bg="#e0f7fa").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_doctor_name = tk.Entry(top_frame, width=20)
entry_doctor_name.grid(row=1, column=1, pady=5)

tk.Label(top_frame, text="Date:", bg="#e0f7fa").grid(row=1, column=2, sticky="w", padx=10, pady=5)
entry_date = tk.Entry(top_frame, width=15)
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
entry_date.grid(row=1, column=3, pady=5)

# Enter button for prescription details
enter_button = tk.Button(top_frame, text="Enter", command=enter_prescription, bg="#4caf50", fg="white", font=("Helvetica", 10, "bold"))
enter_button.grid(row=1, column=4, padx=10, pady=5)

# Clear button for prescription fields
clear_button = tk.Button(top_frame, text="Clear", command=clear_prescription_fields, bg="#b0bec5", fg="black", font=("Helvetica", 10, "bold"))
clear_button.grid(row=1, column=5, padx=10, pady=5)

# Middle Frame for medication details
middle_frame = tk.Frame(root, bg="#f1f8e9", bd=2, relief="solid", padx=20, pady=10)
middle_frame.pack(fill="x", padx=20, pady=10)

tk.Label(middle_frame, text="Prescription Number:", bg="#f1f8e9").grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_presc_number = tk.Entry(middle_frame, width=15)
entry_presc_number.grid(row=0, column=1, pady=5)

tk.Label(middle_frame, text="Medicine Name:", bg="#f1f8e9").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_med_name = tk.Entry(middle_frame, width=20)
entry_med_name.grid(row=1, column=1, pady=5)

tk.Label(middle_frame, text="Quantity:", bg="#f1f8e9").grid(row=0, column=2, sticky="w", padx=10, pady=5)
entry_quantity = tk.Entry(middle_frame, width=10)
entry_quantity.grid(row=0, column=3, pady=5)

tk.Label(middle_frame, text="Disease/Illness:", bg="#f1f8e9").grid(row=1, column=2, sticky="w", padx=10, pady=5)
entry_disease = tk.Entry(middle_frame, width=15)
entry_disease.grid(row=1, column=3, pady=5)

tk.Label(middle_frame, text="Dosage Time:", bg="#f1f8e9").grid(row=1, column=4, sticky="w", padx=10, pady=5)
entry_dosage_time = tk.Entry(middle_frame, width=10)
entry_dosage_time.grid(row=1, column=5, pady=5)

# Add button for medicine details
add_button = tk.Button(middle_frame, text="Add", command=add_medicine, bg="#81c784", fg="white", font=("Helvetica", 10, "bold"))
add_button.grid(row=1, column=6, padx=20, pady=5)

# Bottom Frame for displaying added medicines
bottom_frame = tk.Frame(root, bg="#f9fbe7", bd=2, relief="solid", padx=20, pady=10)
bottom_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

med_tree = ttk.Treeview(bottom_frame, columns=("med_name", "quantity", "disease", "dosage_time"), show="headings")
med_tree.heading("med_name", text="Medicine Name")
med_tree.heading("quantity", text="Quantity")
med_tree.heading("disease", text="Disease/Illness")
med_tree.heading("dosage_time", text="Dosage Time")
med_tree.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()