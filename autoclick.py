from selenium import webdriver

# Create a webdriver instance (you need to download the appropriate webdriver for your browser)
driver = webdriver.Chrome()  # Make sure you have chromedriver installed and in your PATH

# Open the login page
driver.get("https://103.141.218.26/ComfortTechnoNew/home_dashboard.php")  # Replace with the URL of the login page

# Find the username and password input fields by their HTML attributes (replace with actual field attributes)
username_field = driver.find_element_by_id("username")  # Replace "username" with the actual ID of the username input field
password_field = driver.find_element_by_id("password")  # Replace "password" with the actual ID of the password input field

# Enter the username and password
username_field.send_keys("admin@gmail.com")  # Replace "YourUsername" with your actual username
password_field.send_keys("comfort123")  # Replace "YourPassword" with your actual password

# Submit the form (you may need to locate the submit button and click it)
# For example:
# submit_button = driver.find_element_by_id("submit")  # Replace with the actual ID of the submit button
# submit_button.click()

# Close the browser window
# driver.quit()
