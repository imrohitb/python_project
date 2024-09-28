from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome driver
driver = webdriver.Chrome()


# Function to log into the router
def access_router(ip, username, password):
    # Open the router login page
    driver.get(f'http://{ip}')

    # Wait for the username field to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )

    # Enter the username
    driver.find_element_by_id('username').send_keys(username)

    # Enter the password
    driver.find_element_by_id('password').send_keys(password)

    # Click the login button
    driver.find_element_by_id('login').click()


# Router IP address
router_ip = '172.55.21.208:85'  # Replace with your router's IP address

# Call the function to log into the router
access_router(router_ip, 'admin', 'admin')

# Close the browser after the operations are done
driver.quit()
