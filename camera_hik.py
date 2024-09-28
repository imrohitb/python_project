import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth
from requests.exceptions import HTTPError

# Endpoint details
username = 'admin'
password = 'admin123'
ip_camera = '10.109.10.12'
ip_storage = '10.109.10.12'
port = '81'

# URLs for endpoints
camera_status_endpoint = f'http://{ip_camera}:{port}/ISAPI/System/Video/inputs/channels'
hdd_status_endpoint = f'http://{ip_storage}:{port}/ISAPI/ContentMgmt/Storage'

# Function to fetch and print camera status response
def print_camera_status(endpoint):
    try:
        # HTTP Digest Authentication
        auth = HTTPDigestAuth(username, password)

        # GET request with Digest Auth
        response = requests.get(endpoint, auth=auth)

        # Check for HTTP errors
        response.raise_for_status()

        # Parse XML response
        root = ET.fromstring(response.content)

        # Extract and print information for each VideoInputChannel
        # print(f"Response from {endpoint}:")
        for channel in root.findall('.//{http://www.hikvision.com/ver20/XMLSchema}VideoInputChannel'):
            id = channel.find('{http://www.hikvision.com/ver20/XMLSchema}id').text
            res_desc = channel.find('{http://www.hikvision.com/ver20/XMLSchema}resDesc').text.strip()

            # Determine status based on resDesc
            if res_desc == 'NO VIDEO':
                status = 'Not Working'
            else:
                status = 'Working'

            # Print channel details and status
            print(f"Camera {id}: {status}")

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Function to fetch and print HDD status response
def print_hdd_status(endpoint):
    try:
        # HTTP Digest Authentication
        auth = HTTPDigestAuth(username, password)

        # GET request with Digest Auth
        response = requests.get(endpoint, auth=auth)

        # Check for HTTP errors
        response.raise_for_status()

        # Parse XML response
        root = ET.fromstring(response.content)

        # Find the <status> tag
        status_tag = root.find('.//{http://www.hikvision.com/ver20/XMLSchema}status').text.strip()

        # Print the response
        # print(f"Response from {endpoint}:")
        print(f"HDD Status: {status_tag}")
        print()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Fetch and print responses
print_camera_status(camera_status_endpoint)
print_hdd_status(hdd_status_endpoint)
