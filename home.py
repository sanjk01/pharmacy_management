import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk, ImageOps
import os  # Import os to check for file existence

class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Page")
        self.root.geometry("600x400")

        # Load the initial background image
        self.original_image = None
        if os.path.exists('bg.jpg'):
            self.original_image = Image.open('bg.jpg')  # Keep a reference to the original image
        else:
            # Create a placeholder if the image is not found
            self.original_image = Image.new("RGB", (600, 400), "lightblue")  # Placeholder image

        # Create a label to hold the background image
        self.background_label = tk.Label(self.root)
        self.background_label.place(relwidth=1, relheight=1)

        # Create UI Elements with enhanced styles
        title = tk.Label(
            self.root,
            text="Welcome to Our Pharmacy Management System",
            font=("Arial", 28, "bold"),
            fg="black",  # Title text color
            bg="white",  # Title background color
            padx=10,
            pady=10,
            relief="solid",  # Add border
        )
        title.pack(pady=20, padx=10)  # Adding padding around title

         # Create a Logout button in the top-left corner
        logout_button = tk.Button(self.root, text="Logout", command=self.logout, font=("Arial", 16, "bold"), bg="lightgray")
        logout_button.place(x=10, y=10)


        # Create Buttons with double border and bold font
        button_style = {
            "font": ("Arial", 16, "bold"),  # Increase font size and make it bold
            "bd": 2,  # Border width
            "highlightthickness": 2,  # Double border effect
            "relief": "groove",  # Border style
            "bg": "lightgray",  # Button background color
            "activebackground": "gray"  # Button color when clicked
        }

        tk.Button(self.root, text="Pharmacy Management", command=self.open_pharmacy_management, **button_style).pack(pady=10)
        tk.Button(self.root, text="Prescription Information", command=self.open_prescription, **button_style).pack(pady=10)
        tk.Button(self.root, text="Billing", command=self.open_billing, **button_style).pack(pady=10)
        tk.Button(self.root, text="Order Details", command=self.order_details, **button_style).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit, **button_style).pack(pady=10)

        # Bind the configure event to resize the image
        self.root.bind("<Configure>", self.resize_image)

        # Initial resize to fit the current window size
        self.resize_image(None)

    def resize_image(self, event):
        # Resize the background image to fit the window
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Resize the image to fit the window dimensions
        resized_image = ImageOps.fit(self.original_image, (width, height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)  # Update PhotoImage reference
        self.background_label.configure(image=self.bg_image)
        self.background_label.image = self.bg_image  # Keep a reference

    def open_pharmacy_management(self):
        # Call the pharmacy.py file
        subprocess.Popen(['python', 'pharma.py'])

    def open_prescription(self):
        # Call the pharmacy.py file
        subprocess.Popen(['python', 'prescription.py'])

    def open_billing(self):
        # Call the billing.py file
        subprocess.Popen(['python', 'billing.py'])

    def order_details(self):
        subprocess.Popen(['python', 'order_det.py'])

    def logout(self):
        # Close the current window
        self.root.destroy()
        # Open the login page again
        subprocess.Popen(['python', 'login.py'])


if __name__ == "__main__":
    root = tk.Tk()
    home_app = Home(root)
    root.mainloop()