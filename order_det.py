import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import font

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mydata"
)

# Fetch all bills and display them
def fetch_bills():
    cursor = db.cursor()
    cursor.execute("SELECT billing_id, billing_person, customer_name, billing_date, total_amount FROM billing")
    return cursor.fetchall()

# Fetch items for a selected bill
def fetch_bill_items(billing_id):
    cursor = db.cursor()
    cursor.execute("SELECT med_name, quantity, price, total FROM billing_items WHERE billing_id = %s", (billing_id,))
    return cursor.fetchall()

# Update bottom frame with bill items
def display_bill_items(event):
    selected_item = bill_tree.focus()
    if not selected_item:
        return
    
    billing_id = bill_tree.item(selected_item, "values")[0]
    items = fetch_bill_items(billing_id)

    # Clear previous items
    for row in item_tree.get_children():
        item_tree.delete(row)
    
    # Insert new items
    for item in items:
        item_tree.insert("", tk.END, values=item)

# Main application window
root = tk.Tk()
root.title("Order Details")
root.geometry("800x600")
root.configure(bg="#f0f8ff")

# Header
header = tk.Label(root, text="Order Details", font=("Helvetica", 18, "bold"), bg="#4682b4", fg="white")
header.pack(fill="x")

# Frames for layout
top_frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief="solid")
top_frame.pack(fill="x", padx=20, pady=10)
bottom_frame = tk.Frame(root, bg="#f0f8ff", bd=2, relief="solid")
bottom_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# Top frame for billing details
bill_tree = ttk.Treeview(top_frame, columns=("billing_id", "billing_person", "customer_name", "billing_date", "total_amount"), show="headings", height=8)
bill_tree.heading("billing_id", text="Bill ID")
bill_tree.heading("billing_person", text="Billing Person")
bill_tree.heading("customer_name", text="Customer Name")
bill_tree.heading("billing_date", text="Billing Date")
bill_tree.heading("total_amount", text="Total Amount")

# Style adjustments for better visibility
style = ttk.Style()
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
style.configure("Treeview", font=("Helvetica", 10))

# Fill top treeview with bills
bills = fetch_bills()
for bill in bills:
    bill_tree.insert("", tk.END, values=bill)

# Bind click event to display items of the selected bill
bill_tree.bind("<<TreeviewSelect>>", display_bill_items)
bill_tree.pack(fill="x", padx=10, pady=10)

# Bottom frame for displaying items in selected bill
item_tree = ttk.Treeview(bottom_frame, columns=("med_name", "quantity", "price", "total"), show="headings")
item_tree.heading("med_name", text="Medicine Name")
item_tree.heading("quantity", text="Quantity")
item_tree.heading("price", text="Price")
item_tree.heading("total", text="Total")

# More style adjustments
item_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Run the application
root.mainloop()