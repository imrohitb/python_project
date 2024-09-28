import pymysql
import requests
from requests.auth import HTTPDigestAuth
import pandas as pd

# Database connection details
host = "localhost"
username = "root"
password = ""
db_name = "atm_data"

# Connect to the database
connection = pymysql.connect(host=host, user=username, password=password, db=db_name)

# Query to fetch the IP addresses, ports, DVR names, usernames, and passwords
query = "SELECT ip_address, port, DVR_name, username, password FROM sites_master"

# Execute the query and fetch data
with connection.cursor() as cursor:
    cursor.execute(query)
    dvr_data = cursor.fetchall()


# Function to check authentication status
def check_auth(ip, port, username, password):
    url = f"http://{ip}:{port}/"
    try:
        response = requests.get(url, auth=HTTPDigestAuth(username, password), timeout=10)
        if response.status_code == 200:
            return "Working"
        else:
            return "Not Working"
    except requests.exceptions.RequestException:
        return "Not Working"


# Prepare the data for the Excel sheet
data = []
for dvr in dvr_data:
    ip = dvr[0]
    port = dvr[1]
    dvr_name = dvr[2]
    dvr_username = dvr[3]
    dvr_password = dvr[4]
    status = check_auth(ip, port, dvr_username, dvr_password)
    data.append([dvr_name, ip, port, status])

    # Print the status
    print(f"DVR Name: {dvr_name}")
    print(f"IP: {ip}")
    print(f"Status: {status}\n")

# Create a DataFrame and export to Excel
df = pd.DataFrame(data, columns=["DVR Name", "IP Address", "Port", "Status"])
df.to_excel("dvr_status.xlsx", index=False)

print("Results have been exported to dvr_status.xlsx")
