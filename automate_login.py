import pyautogui
import time

# Add a brief pause to ensure your login window is open
time.sleep(3)  # Adjust the sleep time as needed for your window to load

# Locate the 'Username' field and click on it
username_field = pyautogui.locateOnScreen('username_field.png')  # Ensure the file name matches your screenshot
if username_field:
    username_center = pyautogui.center(username_field)
    pyautogui.click(username_center)  # Click the username field
    pyautogui.write('user1')  # Replace with your username

# Locate the 'Password' field and click on it
password_field = pyautogui.locateOnScreen('password_field.png')  # Ensure the file name matches your screenshot
if password_field:
    password_center = pyautogui.center(password_field)
    pyautogui.click(password_center)  # Click the password field
    pyautogui.write('user2')  # Replace with your password

# Locate and click the 'Login' button
login_button = pyautogui.locateOnScreen('login_button.png')  # Ensure the file name matches your screenshot
if login_button:
    login_center = pyautogui.center(login_button)
    pyautogui.click(login_center)  # Click the login button
