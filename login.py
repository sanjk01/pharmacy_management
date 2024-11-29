import mysql.connector
from tkinter import *
from tkinter import messagebox
import subprocess  # Import subprocess to call the home page
import os  # To check for file existence
from PIL import Image, ImageTk, ImageOps  # For handling images

# Function to handle login
def login():
    username = login_username.get()
    password = login_password.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # MySQL password
            database="mydata"
        )
        cursor = conn.cursor()

        # Query to check if the user exists
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", f"Login successful! Welcome {username}")
            conn.close()  # Close the database connection

            # Close the login window
            root.destroy()  # Close the current window

            # Open the home page
            subprocess.Popen(['python', 'home.py'])  # Call home.py
        else:
            messagebox.showerror("Error", "Login incorrect. Please try again.")

        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to register a new user
def register_user():
    username = reg_username.get()
    password = reg_password.get()
    confirm_password = reg_confirm_password.get()
    role = reg_role.get()

    if username == "" or password == "" or confirm_password == "" or role == "":
        messagebox.showerror("Error", "All fields are required")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # MySQL username
            password="root",  # MySQL password
            database="mydata"
        )
        cursor = conn.cursor()

        # Insert the new user into the database
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, role))
        conn.commit()

        messagebox.showinfo("Success", "Registration successful")

        # Clear the fields
        reg_username_entry.delete(0, END)
        reg_password_entry.delete(0, END)
        reg_confirm_password_entry.delete(0, END)
        reg_role_entry.delete(0, END)

        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Switch to registration page
def show_register_page():
    login_frame.place_forget()
    register_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Switch to login page
def show_login_page():
    register_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Create the main window
root = Tk()
root.title("Pharmacy Management System")
root.geometry("500x700")  # Adjusted window height

# Load the initial background image for login page
loginbg_image = None
if os.path.exists('loginbg.jpg'):
    loginbg_image = Image.open('loginbg.jpg')  # Keep a reference to the login background image
else:
    # Create a placeholder if the image is not found
    loginbg_image = Image.new("RGB", (500, 700), "lightblue")  # Placeholder image

# Create a label to hold the background image
background_label = Label(root)
background_label.place(relwidth=1, relheight=1)

# Resize the background image to fit the window
def resize_bg_image(event):
    width = root.winfo_width()
    height = root.winfo_height()

    # Resize the image to fit the window dimensions
    resized_image = ImageOps.fit(loginbg_image, (width, height), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)  # Update PhotoImage reference
    background_label.configure(image=bg_image)
    background_label.image = bg_image  # Keep a reference

# Bind the configure event to resize the background image when the window is resized
root.bind("<Configure>", resize_bg_image)

# Login Frame
login_frame = Frame(root, bg="lightblue", width=400, height=300)  # Light blue background for login frame
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center the login frame

Label(login_frame, text="Login", font=('Arial', 30), fg="black", bg="lightblue").grid(row=0, column=0, columnspan=2, pady=(30, 10))

# Username and Password for Login
Label(login_frame, text="Username", fg="black", bg="lightblue", font=('Arial', 16)).grid(row=1, column=0, padx=10, pady=(20, 5))
login_username = Entry(login_frame, font=('Arial', 16), width=20, highlightthickness=0, relief=FLAT)
login_username.grid(row=1, column=1, padx=10, pady=(20, 5))

Label(login_frame, text="Password", fg="black", bg="lightblue", font=('Arial', 16)).grid(row=2, column=0, padx=10, pady=(5, 5))
login_password = Entry(login_frame, show="*", font=('Arial', 16), width=20, highlightthickness=0, relief=FLAT)
login_password.grid(row=2, column=1, padx=10, pady=(5, 20))

# Login Button
login_button = Button(login_frame, text="Login", command=login, font=('Arial', 16), width=10, bg="#FFB2D5", relief=FLAT)
login_button.grid(row=3, column=1, pady=10)

# Register redirect
Button(login_frame, text="Register", command=show_register_page, font=('Arial', 16), width=10, bg="#FF88C2", relief=FLAT).grid(row=4, column=1, pady=5)

# Registration Frame
register_frame = Frame(root, bg="lightblue", width=400, height=300)  # Light blue background for register frame
register_frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center the register frame

Label(register_frame, text="Register", font=('Arial', 30), fg="black", bg="lightblue").grid(row=0, column=0, columnspan=2, pady=(30, 10))

# Username, Password, Confirm Password, and Role for Registration
Label(register_frame, text="Username", fg="black", bg="lightblue", font=('Arial', 16)).grid(row=1, column=0, padx=10, pady=(20, 5))
reg_username = StringVar()
reg_username_entry = Entry(register_frame, textvariable=reg_username, font=('Arial', 16), width=20, relief=FLAT)
reg_username_entry.grid(row=1, column=1, padx=10, pady=(20, 5))

Label(register_frame, text="Password", fg="black", bg="lightblue", font=('Arial', 16)).grid(row=2, column=0, padx=10, pady=(5, 5))
reg_password = StringVar()
reg_password_entry = Entry(register_frame, textvariable=reg_password, show="*", font=('Arial', 16), width=20, relief=FLAT)
reg_password_entry.grid(row=2, column=1, padx=10, pady=(5, 5))

Label(register_frame, text="Confirm Password", fg="black", bg="lightblue", font=('Arial', 16)).grid(row=3, column=0, padx=10, pady=(5, 5))
reg_confirm_password = StringVar()
reg_confirm_password_entry = Entry(register_frame, textvariable=reg_confirm_password, show="*", font=('Arial', 16), width=20, relief=FLAT)
reg_confirm_password_entry.grid(row=3, column=1, padx=10, pady=(5, 20))

Label(register_frame, text="Role", fg="black", bg="lightblue", font=('Arial', 16)).grid(row=4, column=0, padx=10, pady=(5, 5))
reg_role = StringVar()
reg_role_entry = Entry(register_frame, textvariable=reg_role, font=('Arial', 16), width=20, relief=FLAT)
reg_role_entry.grid(row=4, column=1, padx=10, pady=(5, 20))

# Register Button
register_button = Button(register_frame, text="Register", command=register_user, font=('Arial', 16), width=10, bg="#FF88C2", relief=FLAT)
register_button.grid(row=5, column=1, pady=10)

# Login redirect
Button(register_frame, text="Back to Login", command=show_login_page, font=('Arial', 16), width=15, bg="#FF88C2", relief=FLAT).grid(row=6, column=1, pady=5)

# Initially hide register frame
register_frame.place_forget()

# Start the Tkinter main loop
root.mainloop() 