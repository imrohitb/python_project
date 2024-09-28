import requests
from requests.auth import HTTPDigestAuth

# NVR credentials and URL
nvr_url = "http://10.109.10.105:81/ISAPI/System/time/ntpServers/1"
username = "admin"
password = "css12345"

# NTP server configuration XML
ntp_config_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<NTPServer version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">
    <id>1</id>
    <addressingFormatType>hostname</addressingFormatType>
    <hostName>192.168.100.24</hostName>
    <ipAddress></ipAddress>
    <ipv6Address></ipv6Address>
    <portNo>123</portNo>
    <synchronizeInterval>1</synchronizeInterval>
</NTPServer>
"""

# Send PUT request to set NTP server
response = requests.put(
    nvr_url,
    data=ntp_config_xml,
    auth=HTTPDigestAuth(username, password),
    headers={"Content-Type": "application/xml"}
)

# Check response
if response.status_code == 200:
    print("NTP server set successfully.")
else:
    print(f"Failed to set NTP server. Status code: {response.status_code}")
    print(response.text)
