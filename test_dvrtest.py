from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(25)  # Implicit wait
    return driver

def teardown_browser(driver):
    driver.quit()

def double_click_element(driver, by, value):
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((by, value))
    )
    actions = ActionChains(driver)
    actions.double_click(element).perform()

def main():
    driver = setup_browser()
    try:
        driver.get("http://10.109.66.246:81/")
        driver.set_window_size(1552, 840)
        
        # Login
        double_click_element(driver, By.ID, "loginUsername-inputEl")
        driver.find_element(By.ID, "loginUsername-inputEl").send_keys("admin")
        driver.find_element(By.ID, "loginPassword-inputEl").send_keys("css@12345")
        driver.find_element(By.ID, "loginButton-btnIconEl").click()
        
        # Wait for elements to be clickable before interacting
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "button-1039-btnIconEl"))
        ).click()
        
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#menuitem-1027-textEl > span"))
        ).click()
        
        driver.execute_script("window.scrollTo(0,0)")
        
        # Click elements with potential interactions
        elements_to_double_click = [
            "ext-gen1151", "combobox-1061-inputEl", "ext-comp-1062-inputEl",
            "ext-comp-1059-innerCt", "ext-comp-1076-btnIconEl",
            "ext-gen1159", "textfield-1090-inputEl", "ext-comp-1091-inputEl",
            "textfield-1094-inputEl", "ext-comp-1084-innerCt", "textfield-1095-inputEl",
            "textfield-1097-inputEl", "combobox-1110-inputEl", "ext-gen1459",
            "checkbox-1131-inputEl", "ext-comp-1157-btnIconEl", "ext-comp-1154-btnIconEl"
        ]
        
        for element_id in elements_to_double_click:
            double_click_element(driver, By.ID, element_id)
        
        # Additional actions if needed
        driver.find_element(By.ID, "textfield-1095-inputEl").send_keys("cam@12345")
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "ext-comp-1154-btnIconEl"))
        ).click()
        
    finally:
        teardown_browser(driver)

if __name__ == "__main__":
    main()
