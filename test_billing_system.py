import unittest
from unittest.mock import MagicMock, patch
from billing import Billing  # Import your Billing class
import tkinter as tk
from tkinter import messagebox

class TestBillingSystem(unittest.TestCase):

    @patch('billing_system.mysql.connector.connect')  # Mock MySQL connection
    @patch('billing_system.messagebox.showinfo')  # Mock messagebox.showinfo
    def test_add_item_success(self, mock_showinfo, mock_connect):
        # Mock database cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Set up the mock data for the pharmacy
        mock_cursor.fetchone.return_value = (10.0, 100)  # Price per unit: 10.0, Available Quantity: 100

        # Create the Tkinter root window (mocked)
        root = tk.Tk()
        app = Billing(root)

        # Simulate user input
        app.billing_person_var.set("John Doe")
        app.customer_name_var.set("Jane Smith")
        app.med_name_var.set("Aspirin")
        app.quantity_var.set(5)

        # Call the add_item method to simulate adding a medicine
        app.add_item()

        # Check if the cursor execute method was called to fetch the medicine details from the database
        mock_cursor.execute.assert_called_with(
            "SELECT Price, product FROM pharmacy WHERE MedName = %s", ('Aspirin',)
        )

        # Check if the price and total were updated correctly
        self.assertEqual(app.total_bill_var.get(), 50.0)  # 5 * 10.0 (price per unit)
        mock_showinfo.assert_called_with(
            "Item Added", "Price per Unit: $10.00\nTotal: $50.00"
        )

    @patch('billing_system.mysql.connector.connect')  # Mock MySQL connection
    def test_finish_billing(self, mock_connect):
        # Mock database cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Set up mock return for SQL queries
        mock_cursor.lastrowid = 123  # Fake last inserted ID for billing

        # Create the Tkinter root window (mocked)
        root = tk.Tk()
        app = Billing(root)

        # Simulate user input
        app.billing_person_var.set("John Doe")
        app.customer_name_var.set("Jane Smith")
        app.med_name_var.set("Aspirin")
        app.quantity_var.set(5)
        app.add_item()  # Adding the item first

        # Now call finish_billing method to simulate the user completing the billing
        app.finish_billing()

        # Check if the billing details were inserted into the database
        mock_cursor.execute.assert_any_call(
            "INSERT INTO billing (billing_person, customer_name, billing_date, total_amount) VALUES (%s, %s, %s, %s)",
            ('John Doe', 'Jane Smith', app.billing_date_entry.get(), 50.0)
        )

        # Check if the billing items were inserted into the billing_items table
        mock_cursor.execute.assert_any_call(
            "INSERT INTO billing_items (billing_id, med_name, quantity, price, total) VALUES (%s, %s, %s, %s, %s)",
            (123, 'Aspirin', 5, 10.0, 50.0)
        )

        # Verify that changes were committed to the database
        mock_connect.return_value.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
