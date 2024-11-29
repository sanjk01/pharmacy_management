import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import datetime

class Billing:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f8ff")

        # Variables
        self.billing_person_var = tk.StringVar()
        self.customer_name_var = tk.StringVar()
        self.billing_date_var = tk.StringVar()
        self.med_name_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.price_var = tk.DoubleVar()
        self.total_var = tk.DoubleVar()
        self.total_bill_var = tk.DoubleVar(value=0.0)

        # Create UI Elements
        title = tk.Label(self.root, text="Billing System", font=("Arial", 24, "bold"), bg="#f0f8ff")
        title.pack(pady=10)

        # Billing Info Frame
        billing_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="#f0f8ff")
        billing_frame.place(x=20, y=50, width=760, height=150)

        tk.Label(billing_frame, text="Billing Person:", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(billing_frame, textvariable=self.billing_person_var, font=("Arial", 12)).grid(row=0, column=1, padx=10)

        tk.Label(billing_frame, text="Customer Name:", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=0, column=2, padx=10, pady=10)
        tk.Entry(billing_frame, textvariable=self.customer_name_var, font=("Arial", 12)).grid(row=0, column=3, padx=10)

        tk.Label(billing_frame, text="Billing Date:", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10)
        self.billing_date_entry = tk.Entry(billing_frame, font=("Arial", 12))
        self.billing_date_entry.grid(row=1, column=1, padx=10)
        self.billing_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Set default date to today
        self.billing_date_var.set(self.billing_date_entry.get())

        # Medicine Info Frame
        medicine_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="#f0f8ff")
        medicine_frame.place(x=20, y=210, width=760, height=250)

        tk.Label(medicine_frame, text="Medicine Name:", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(medicine_frame, textvariable=self.med_name_var, font=("Arial", 12)).grid(row=0, column=1, padx=10)

        tk.Label(medicine_frame, text="Quantity:", font=("Arial", 12, "bold"), bg="#f0f8ff").grid(row=0, column=2, padx=10, pady=10)
        tk.Entry(medicine_frame, textvariable=self.quantity_var, font=("Arial", 12)).grid(row=0, column=3, padx=10)

        tk.Button(medicine_frame, text="Add", command=self.add_item, font=("Arial", 12, "bold"), bg="#98fb98").grid(row=2, column=0, columnspan=2, pady=10, padx=10)
        tk.Button(medicine_frame, text="Finish", command=self.finish_billing, font=("Arial", 12, "bold"), bg="#ff6347").grid(row=2, column=2, columnspan=2, pady=10)

        # Total Amount Label
        self.total_amount_label = tk.Label(self.root, text="Total Amount: $0.00", font=("Arial", 14, "bold"), bg="#f0f8ff")
        self.total_amount_label.place(x=20, y=480)

        # Billing Items Table
        self.billing_table = ttk.Treeview(self.root, columns=("med_name", "quantity", "price", "total"), show="headings")
        self.billing_table.heading("med_name", text="Medicine Name")
        self.billing_table.heading("quantity", text="Quantity")
        self.billing_table.heading("price", text="Price")
        self.billing_table.heading("total", text="Total")
        self.billing_table.place(x=20, y=520, width=760, height=150)

    def add_item(self):
        med_name = self.med_name_var.get()

        # Convert quantity from string to int
        try:
            quantity = int(self.quantity_var.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
            return

        # Check for availability in pharmacy when "Add" is clicked
        conn = mysql.connector.connect(host="localhost", username="root", password="root", database="mydata")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT Price, product FROM pharmacy WHERE MedName = %s", (med_name,))
        result = my_cursor.fetchone()

        if result is None:
            messagebox.showerror("Error", "Medicine not found in pharmacy")
            conn.close()
            return

        price_per_unit = float(result[0])  # Convert to float
        available_quantity = int(result[1])  # Convert to int

        if quantity > available_quantity:
            messagebox.showerror("Error", f"Insufficient quantity available. Available: {available_quantity}")
            conn.close()
            return
        

        #TRIGGER SIMULATION WITH FRONTEND
        # Update the quantity in the pharmacy database  
        new_quantity = available_quantity - quantity
        my_cursor.execute("UPDATE pharmacy SET product = %s WHERE MedName = %s", (new_quantity, med_name))
        conn.commit()  # Commit the update to the database

        total = quantity * price_per_unit  # Now `price_per_unit` is a float
        self.total_var.set(total)

        # Display price and total in a message box
        messagebox.showinfo("Item Added", f"Price per Unit: ${price_per_unit:.2f}\nTotal: ${total:.2f}")

        # Update total bill
        current_total = self.total_bill_var.get()
        new_total = current_total + total
        self.total_bill_var.set(new_total)
        self.total_amount_label.config(text=f"Total Amount: ${new_total:.2f}")

        # Insert into billing items table in the UI
        self.billing_table.insert("", "end", values=(med_name, quantity, price_per_unit, total))

        conn.close()

        # Clear medicine fields
        self.med_name_var.set("")  # Clear medicine name
        self.quantity_var.set(0)    # Clear quantity

    def finish_billing(self):
        billing_person = self.billing_person_var.get()
        customer_name = self.customer_name_var.get()
        billing_date = self.billing_date_entry.get()
        
        if not billing_person or not customer_name:
            messagebox.showerror("Error", "Please enter billing person and customer name")
            return
        
        # Insert billing details into billing table
        conn = mysql.connector.connect(host="localhost", username="root", password="root", database="mydata")
        my_cursor = conn.cursor()
        my_cursor.execute("INSERT INTO billing (billing_person, customer_name, billing_date, total_amount) VALUES (%s, %s, %s, %s)",
                          (billing_person, customer_name, billing_date, self.total_bill_var.get()))
        conn.commit()

        # Retrieve the last inserted billing_id
        billing_id = my_cursor.lastrowid

        # Now insert all items in the billing_items table with the retrieved billing_id
        for row in self.billing_table.get_children():
            item = self.billing_table.item(row)
            med_name, quantity, price_per_unit, total = item['values']
            my_cursor.execute("INSERT INTO billing_items (billing_id, med_name, quantity, price, total) VALUES (%s, %s, %s, %s, %s)",
                              (billing_id, med_name, quantity, price_per_unit, total))
        
        conn.commit()
        conn.close()

        # Clear all fields after finishing billing
        self.billing_person_var.set("")  # Clear billing person
        self.customer_name_var.set("")    # Clear customer name
        self.billing_date_entry.delete(0, tk.END)  # Clear billing date
        self.billing_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Reset to today
        self.total_bill_var.set(0.0)     # Reset total bill
        self.total_amount_label.config(text="Total Amount: $0.00")  # Reset total amount label
        self.billing_table.delete(*self.billing_table.get_children())  # Clear table

        messagebox.showinfo("Billing Complete", "The billing has been successfully completed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Billing(root)
    root.mainloop()
