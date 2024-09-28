from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

# DVR credentials
url = "http://10.109.66.246:81/"
username = "admin"
password = "css@12345"

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=Service('C:\\Users\\Rohit J Bhardwaj\\Downloads\\chromedriver-win64\\chromedriver.exe'))

# Open the DVR URL
driver.get(url)

# Wait for the page to load (adjust the timeout as needed)
wait = WebDriverWait(driver, 10)

# Find and fill the username and password fields
wait.until(EC.presence_of_element_located((By.ID, "loginUsername-inputEl"))).send_keys(username)
wait.until(EC.presence_of_element_located((By.ID, "loginPassword-inputEl"))).send_keys(password)

# Click the login button
wait.until(EC.element_to_be_clickable((By.ID, "loginButton-btnIconEl"))).click()

# Wait for the next page to load
time.sleep(5)

# Click the element with ID 'button-1039-btnIconEl'
try:
    target_button = wait.until(EC.element_to_be_clickable((By.ID, "button-1039-btnIconEl")))
    target_button.click()
    print("Clicked the target button successfully.")
except Exception as e:
    print(f"Error clicking the button: {e}")

# Close the browser after use
# driver.quit()
