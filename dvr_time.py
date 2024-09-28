import mysql.connector
import requests
from requests.auth import HTTPDigestAuth


# Function to get current DVR time
def get_dvr_time(ip, username, password):
    url = f"http://{ip}:81/cgi-bin/global.cgi?action=getCurrentTime"
    try:
        response = requests.get(url, auth=HTTPDigestAuth(username, password))
        if response.status_code == 200:
            return True, response.text
        else:
            return False, f"Failed to fetch DVR time, HTTP Status Code: {response.status_code}\nResponse: {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"An error occurred: {e}"


# Function to fetch DVR details from the database for a specific IP
def fetch_dvr_details(ip_address):
    connection = mysql.connector.connect(
        host='localhost',  # replace with your database host
        user='root',  # replace with your database username
        password='',  # replace with your database password
        database='atm_data'  # replace with your database name
    )

    cursor = connection.cursor()
    query = "SELECT IP, Username, Password, Port FROM dvr_master WHERE IP = %s AND dvr_type = 'Dahuva'"
    cursor.execute(query, (ip_address,))
    dvr_details = cursor.fetchone()

    cursor.close()
    connection.close()

    return dvr_details


# Fetch DVR details and get DVR time for the specific IP
def get_and_print_dvr_time(ip_address):
    dvr_details = fetch_dvr_details(ip_address)

    if dvr_details:
        ip, username, password, port = dvr_details
        print(f"Fetching DVR time for IP: {ip}")
        connected, response = get_dvr_time(ip, username, password)
        if connected:
            print(f"DVR Time for IP {ip}: {response}")
        else:
            print(f"Failed to fetch DVR time for IP {ip}: {response}")
    else:
        print(f"No DVR found with IP {ip_address} and type 'Dahuva'.")


# Define the specific IP to fetch
specific_ip = "10.109.70.172"

# Run the process
get_and_print_dvr_time(specific_ip)
