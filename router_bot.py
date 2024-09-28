import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
import time

# Function to automate login and fill cloud details
def automate_router(ip_address):
    driver = webdriver.Chrome()
    
    try:
        # Open router login page
        driver.get(f"http://{ip_address}:85")
        time.sleep(2)

        # Maximize the browser window
        driver.maximize_window()

        # Login to the router
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")

        username_input.send_keys("admin")
        password_input.send_keys("admin")

        # Submit the login form
        login_button = driver.find_element(By.ID, "login")
        login_button.click()

        time.sleep(10)  # Wait for the page to load

        # Navigate to Application section
        application_menu = driver.find_element(By.LINK_TEXT, "Applications")
        application_menu.click()
        time.sleep(5)

        # Click on Cloud
        cloud_menu = driver.find_element(By.LINK_TEXT, "Cloud")
        cloud_menu.click()
        time.sleep(5)

        # Fill in the Cloud details
        cloud_username = driver.find_element(By.NAME, "peer")
        cloud_username.clear()
        cloud_username.send_keys("103.141.218.138")

        # Submit the Cloud form
        submit_button = driver.find_element(By.NAME, "save_button")
        submit_button.click()

        time.sleep(5)  # Wait for the action to complete

        return (ip_address, "Success")

    except Exception as e:
        print(f"Failed for {ip_address}: {e}")
        return (ip_address, "Failed")

    finally:
        # Close the browser
        driver.quit()

# Read the router IPs from the Excel file located in the project folder
def read_ips_from_excel():
    df = pd.read_excel('router_ips.xlsx')  # Ensure 'router_ips.xlsx' is in the project folder
    return df['IP'].tolist()

# Function to save the results in a new Excel file
def save_results_to_excel(results):
    df = pd.DataFrame(results, columns=["IP", "Result"])
    df.to_excel("router_results.xlsx", index=False)

# Main function to run the automation in 5 threads
def main():
    # Read IPs from the Excel file
    ip_addresses = read_ips_from_excel()  # Now this returns the IPs

    # Run 5 threads
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit the automation task for each IP and collect the results
        results = list(executor.map(automate_router, ip_addresses))

    # Save the results to Excel
    save_results_to_excel(results)

if __name__ == "__main__":
    main()
