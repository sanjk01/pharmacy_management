import tkinter as tk
from tkinter import messagebox
import unittest
from unittest.mock import patch
import time

# Define the login function that opens the window and handles login
def login(credential_check):
    def check_credentials():
        username = login_username.get()
        password = login_password.get()

        # Call the credential check function passed to simulate different scenarios
        credential_check(username, password)
        
        root.quit()  # Close the window after checking credentials

    # Set up the Tkinter window
    root = tk.Tk()
    root.title("Login")

    # Username and password fields
    login_username = tk.Entry(root)
    login_username.pack(pady=10)
    login_password = tk.Entry(root, show="*")
    login_password.pack(pady=10)

    # Login button
    login_button = tk.Button(root, text="Login", command=check_credentials)
    login_button.pack(pady=10)

    # Auto-insert credentials for testing purposes
    root.after(500, lambda: login_username.insert(0, 'user1'))  # Insert username after 500ms
    root.after(1000, lambda: login_password.insert(0, 'password1'))  # Insert password after 1000ms

    root.mainloop()  # Start Tkinter event loop

# Function to simulate login logic for correct or incorrect credentials
def simulate_login(username, password):
    if username == "user1" and password == "password1":
        messagebox.showinfo("Success", "Login successful! Welcome user1")
    else:
        messagebox.showerror("Error", "Login incorrect. Please try again.")

# Unit tests for login functionality
class TestLoginFunction(unittest.TestCase):
    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    def test_successful_login(self, mock_showinfo, mock_showerror):
        # Start the login process for correct credentials
        login(simulate_login)
        
        # Wait for the message box to appear
        time.sleep(2)  # Allow time for the interaction to happen

        # Test if the success message was called
        mock_showinfo.assert_called_with("Success", "Login successful! Welcome user1")

    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    def test_incorrect_login(self, mock_showinfo, mock_showerror):
        # Start the login process with incorrect credentials
        login(simulate_login)

        # Wait for the message box to appear
        time.sleep(2)  # Allow time for the interaction to happen

        # Test if the error message was called
        mock_showerror.assert_called_with("Error", "Login incorrect. Please try again.")

# Run the tests
if __name__ == "__main__":
    unittest.main()
