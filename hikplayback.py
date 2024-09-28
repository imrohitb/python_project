import requests
import xml.etree.ElementTree as ET

url = "http://10.109.8.225:81/ISAPI/ContentMgmt/storage"
username = "admin"
password = "admin123"

try:
    # Send GET request with HTTP Digest authentication
    response = requests.get(url, auth=requests.auth.HTTPDigestAuth(username, password))
    response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

    # Parse the XML response
    root = ET.fromstring(response.content)

    # Define the namespace
    ns = {'ns': 'http://www.hikvision.com/ver20/XMLSchema'}

    # Find the status of HDD
    status_elem = root.find('.//ns:status', namespaces=ns)

    if status_elem is not None:
        status = status_elem.text.strip().lower()
        if status == 'ok':
            print("HDD is working.")
        else:
            print(f"HDD status: {status}")
    else:
        print("Status element not found in the response XML.")

except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Request Exception: {err}")
except ET.ParseError as parse_err:
    print(f"XML Parsing Error: {parse_err}")
except Exception as e:
    print(f"An error occurred: {e}")
