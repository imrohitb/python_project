from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Create a new Chrome WebDriver instance
browser = webdriver.Chrome()

# Open the Chrome browser
# Visit the specified webpage
url = "http://172.55.21.208:85/gui/status_main.cgi"
browser.get(url)

# Input the username and password by Name attribute
username_input = browser.find_element(By.ID, 'username')
password_input = browser.find_element(By.ID, 'password')

# Input your username and password here
username_input.send_keys('admin')
password_input.send_keys('admin')

# Locate and click the "Log in" button by NAME attribute
login_button = browser.find_element(By.ID, 'login')
login_button.click()
time.sleep(10)

# Keep the browser open until manually closed
# It's generally not a good practice to use an infinite loop like this
# Consider using browser.quit() to close the browser when done
