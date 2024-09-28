from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Path to the ChromeDriver executable
driver = webdriver.Chrome()

try:
    # Open the webpage
    driver.get('http://10.109.10.149:81')  # Replace with your URL

    # Wait until the username field is present
    wait = WebDriverWait(driver, 60)  # 10 seconds timeout
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'loginUsername-inputEl')))  # Use the appropriate locator

    # Enter the username
    wait = WebDriverWait(driver, 60)
    username_field.send_keys('admin')  # Replace with your username
    time.sleep(20)

    # Wait until the password field is present
    wait = WebDriverWait(driver, 60)
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'loginPassword-inputEl')))  # Use the appropriate locator
    time.sleep(20)
    # Enter the password
    password_field.send_keys('admin123')  # Replace with your password

    # Optionally, submit the form
    password_field.send_keys(Keys.RETURN)  # Press Enter to submit the form

finally:
    # Close the WebDriver
    driver.quit()
