import requests
from requests.auth import HTTPDigestAuth

# NVR details
hdd_status_url = "http://172.51.0.235:81/ISAPI/System/workingstatus/hdStatus?format=json"
username = "admin"
password = "css12345"

# Send the request to get HDD status
response = requests.get(hdd_status_url, auth=HTTPDigestAuth(username, password))

# Check the response
if response.status_code == 200:
    hdd_status = response.json()
    print("HDD Status:")
    print(hdd_status)  # This will print the JSON response with HDD status

    # Extract and print specific status details
    if 'HDD' in hdd_status:
        for hdd in hdd_status['HDD']:
            status = hdd.get('status', 'Unknown')
            capacity = hdd.get('capacity', 'Unknown')
            free_space = hdd.get('freeSpace', 'Unknown')
            print(f"HDD Status: {status}")
            print(f"Capacity: {capacity}")
            print(f"Free Space: {free_space}")
    else:
        print("No HDD information found.")
else:
    print(f"Failed to get HDD status. Status code: {response.status_code}")
    print(response.text)
