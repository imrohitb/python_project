import requests
from requests.auth import HTTPDigestAuth

# DVR credentials and IP details
username = "admin"
password = "admin@123"
ip = "172.55.26.15"
port = "81"

# API URL to get the current DVR time
url = f"http://{ip}:{port}/ISAPI/System/time"

# Make the request using HTTP Digest authentication
response = requests.get(url, auth=HTTPDigestAuth(username, password))

if response.status_code == 200:
    print("DVR Time:", response.text)
else:
    print("Failed to get DVR time. Status code:", response.status_code)
    print("Response:", response.text)