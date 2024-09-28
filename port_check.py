import os
import pandas as pd
import socket
import subprocess
import requests

# Function to check port status
def check_port_status(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return "Open" if result == 0 else "Closed"

# Function to ping a URL
def ping_url(url):
    try:
        subprocess.check_output(["ping", "-c", "1", url])
        return "Reachable"
    except subprocess.CalledProcessError:
        return "Unreachable"

# Get the script's directory
script_directory = os.path.dirname(os.path.realpath(__file__))

# Read URLs and Ports from Excel in the same directory as the script
excel_file_path = os.path.join(script_directory, 'urls.xlsx')
df = pd.read_excel(excel_file_path)

# Convert the comma-separated ports to a list of integers
df['Ports'] = df['Ports'].apply(lambda x: [int(port) for port in str(x).split(',')])

# Print Port Status and Ping Status for each URL
for index, row in df.iterrows():
    print(f"URL: {row['URL']}")
    for port in row['Ports']:
        port_status = check_port_status(row['URL'], port)
        print(f"  Port {port} Status: {port_status}")
    ping_status = ping_url(row['URL'])
    print(f"  Ping Status: {ping_status}")
    print()
