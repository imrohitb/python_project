from selenium import webdriver
from selenium.webdriver.edge.service import Service

edge_driver_path = "D:\Rohit\msedgedriver.exe"
service = Service(executable_path=edge_driver_path)

# Set up Edge WebDriver
driver = webdriver.Edge(service=service)

# Navigate to the router's page
driver.get("http://www.google.com")
